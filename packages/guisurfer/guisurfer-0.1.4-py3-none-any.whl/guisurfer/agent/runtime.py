import base64
import os
from cryptography.fernet import Fernet
from dataclasses import dataclass, field
from typing import List, Optional
import uuid
import time
import json
import tempfile

from google.oauth2 import service_account
from google.cloud import container_v1
from google.auth.transport.requests import Request
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from agentdesk.vm import DesktopVM

from guisurfer.db.conn import WithDB
from guisurfer.db.models import AgentRuntimeRecord
from guisurfer.server.models import AgentRuntimeModel
from guisurfer.server.key import SSHKeyPair
from .types import AgentType
from .base import TaskAgentInstance
from .env import (
    HUB_SERVER_ENV,
    AGENTD_ADDR_ENV,
    AGENTD_PRIVATE_SSH_KEY_ENV,
    AGENTSEA_HUB_URL_ENV,
)


@dataclass
class AgentRuntime(WithDB):
    """A runtime for agents"""

    name: str
    provider: str
    owner_id: str
    credentials: dict
    created: float = field(default_factory=lambda: time.time())
    updated: float = field(default_factory=lambda: time.time())
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: dict = field(default_factory=lambda: {})

    def __post_init__(self) -> None:
        self.credentials = self.encrypt_credentials(self.credentials)
        self.save()

    @classmethod
    def get_encryption_key(cls) -> str:
        return os.environ["ENCRYPTION_KEY"]

    def encrypt_credentials(self, credentials: str) -> str:
        key = self.get_encryption_key()
        fernet = Fernet(key)
        encrypted_credentials = fernet.encrypt(json.dumps(credentials).encode())
        return base64.b64encode(encrypted_credentials).decode()

    @classmethod
    def decrypt_credentials(cls, encrypted_credentials: str) -> str:
        key = cls.get_encryption_key()
        fernet = Fernet(key)
        decrypted_credentials = fernet.decrypt(base64.b64decode(encrypted_credentials))
        return json.loads(decrypted_credentials.decode())

    def to_record(self) -> AgentRuntimeRecord:
        return AgentRuntimeRecord(
            id=self.id,
            owner_id=self.owner_id,
            name=self.name,
            provider=self.provider,
            credentials=self.credentials,
            created=self.created,
            updated=self.updated,
            metadata_=json.dumps(self.metadata) if self.metadata else None,
            full_name=f"{self.owner_id}/{self.name}",
        )

    @classmethod
    def from_record(cls, record: AgentRuntimeRecord) -> "AgentRuntime":
        obj = cls.__new__(cls)
        obj.id = record.id
        obj.name = record.name
        obj.provider = record.provider
        obj.credentials = record.credentials
        obj.created = record.created
        obj.owner_id = record.owner_id
        obj.updated = record.updated
        obj.metadata = json.loads(record.metadata_) if record.metadata_ else {}
        return obj

    def to_schema(self) -> AgentRuntimeModel:
        return AgentRuntimeModel(
            id=self.id,
            name=self.name,
            provider=self.provider,
            created=self.created,
            updated=self.updated,
            metadata=self.metadata if self.metadata else {},
        )

    def save(self) -> None:
        for db in self.get_db():
            db.merge(self.to_record())
            db.commit()

    @classmethod
    def find(cls, **kwargs) -> List["AgentRuntime"]:
        for db in cls.get_db():
            records = db.query(AgentRuntimeRecord).filter_by(**kwargs).all()
            return [cls.from_record(record) for record in records]

    @classmethod
    def delete(cls, name: str, owner_id: str) -> None:
        for db in cls.get_db():
            record = (
                db.query(AgentRuntimeRecord)
                .filter_by(name=name, owner_id=owner_id)
                .first()
            )
            if record:
                db.delete(record)
                db.commit()

    def status(self, name: str) -> str:
        if self.provider == "gke":
            creds: dict = self.decrypt_credentials(self.credentials)
            service_account_json = creds.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
            if not service_account_json:
                raise ValueError(
                    "GOOGLE_APPLICATION_CREDENTIALS_JSON not found in credentials"
                )

            cluster_name = self.metadata.get("CLUSTER_NAME")
            if not cluster_name:
                raise ValueError("CLUSTER_NAME not found in metadata")

            region = self.metadata.get("REGION")
            if not region:
                raise ValueError("REGION not found in metadata")

            namespace = self.metadata.get("NAMESPACE", "default")

            service_account_info: dict = json.loads(service_account_json)
            project_id = service_account_info.get("project_id")
            if not project_id:
                raise ValueError("project_id not found in credentials")

            credentials = service_account.Credentials.from_service_account_info(
                service_account_info
            )

            gke_service = container_v1.ClusterManagerClient(credentials=credentials)

            cluster_request = container_v1.GetClusterRequest(
                name=f"projects/{project_id}/locations/{region}/clusters/{cluster_name}"
            )
            cluster = gke_service.get_cluster(request=cluster_request)

            # Decode the CA certificate and store it temporarily
            ca_cert = base64.b64decode(cluster.master_auth.cluster_ca_certificate)
            with tempfile.NamedTemporaryFile(delete=False) as temp_ca_file:
                temp_ca_file.write(ca_cert)
                ca_cert_path = temp_ca_file.name

            # Configure kubectl using the cluster details and the temporary CA certificate
            configuration = client.Configuration()
            configuration.host = f"https://{cluster.endpoint}:443"
            configuration.verify_ssl = True
            configuration.ssl_ca_cert = ca_cert_path

            configuration.api_key = {"authorization": f"Bearer {credentials.token}"}

            client.Configuration.set_default(configuration)
            v1 = client.CoreV1Api()
            try:
                pod: client.V1Pod = v1.read_namespaced_pod(
                    name=name, namespace=namespace
                )
                status: client.V1PodStatus = pod.status
            except ApiException as e:
                print(f"Exception when calling CoreV1Api->read_namespaced_pod: {e}")

            os.unlink(ca_cert_path)

            return status

    def run(
        self,
        name: str,
        type: str,
        desktop: str,
        owner_id: str,
        envs: dict = {},
        secrets: dict = {},
        metadata: dict = {},
        wait_ready: bool = True,
        icon: Optional[str] = None,
    ) -> TaskAgentInstance:
        agent_types = AgentType.find(name=type)
        if not agent_types:
            raise ValueError(f"No agent type found with name {type}")
        agent_type = agent_types[0]

        desktop_vm = DesktopVM.get(name=desktop)
        if not desktop_vm:
            raise ValueError(f"No desktop found with name {desktop}")

        task_agents = TaskAgentInstance.find(name=name, owner_id=owner_id)
        if not task_agents:
            raise ValueError(f"Could not find task agent instance '{name}'")
        task_agent = task_agents[0]

        SERVER_ADDRESS = os.getenv("SERVER_ADDRESS")
        if not SERVER_ADDRESS:
            raise ValueError("$SERVER_ADDRESS environment variable must be set")

        if self.provider == "gke":
            print("creating gke agent...")
            creds: dict = self.decrypt_credentials(self.credentials)
            service_account_json = creds.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
            if not service_account_json:
                raise ValueError(
                    "GOOGLE_APPLICATION_CREDENTIALS_JSON not found in credentials"
                )

            cluster_name = self.metadata.get("CLUSTER_NAME")
            if not cluster_name:
                raise ValueError("CLUSTER_NAME not found in metadata")

            region = self.metadata.get("REGION")
            if not region:
                raise ValueError("REGION not found in metadata")

            namespace = self.metadata.get("NAMESPACE", "default")

            service_account_info = json.loads(service_account_json)
            print("\nservice account info: ", service_account_info)

            project_id = service_account_info.get("project_id")
            if not project_id:
                raise ValueError("project_id not found in credentials")

            credentials = service_account.Credentials.from_service_account_info(
                service_account_info
            )

            gke_service = container_v1.ClusterManagerClient(credentials=credentials)

            cluster_request = container_v1.GetClusterRequest(
                name=f"projects/{project_id}/locations/{region}/clusters/{cluster_name}"
            )
            cluster = gke_service.get_cluster(request=cluster_request)

            # Decode the CA certificate and store it temporarily
            ca_cert = base64.b64decode(cluster.master_auth.cluster_ca_certificate)

            # Obtain the access token using the service account credentials
            credentials = service_account.Credentials.from_service_account_info(
                service_account_info,
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )
            credentials.refresh(Request())
            access_token = credentials.token

            kubeconfig = {
                "apiVersion": "v1",
                "kind": "Config",
                "clusters": [
                    {
                        "name": cluster_name,
                        "cluster": {
                            "server": f"https://{cluster.endpoint}",
                            "certificate-authority-data": base64.b64encode(
                                ca_cert
                            ).decode(),
                        },
                    }
                ],
                "contexts": [
                    {
                        "name": cluster_name,
                        "context": {
                            "cluster": cluster_name,
                            "user": cluster_name,
                        },
                    }
                ],
                "current-context": cluster_name,
                "users": [
                    {
                        "name": cluster_name,
                        "user": {
                            "token": access_token,
                        },
                    }
                ],
            }

            # Load the kubeconfig file
            config.load_kube_config_from_dict(config_dict=kubeconfig)

            # Find the SSH key for the desktop VM
            print("finding ssh key...")
            ssh_keys = SSHKeyPair.find(
                owner_id=self.owner_id, public_key=desktop_vm.ssh_key
            )
            if not ssh_keys:
                raise ValueError("No SSH key found for desktop VM")
            ssh_key = ssh_keys[0]
            secrets[AGENTD_PRIVATE_SSH_KEY_ENV] = ssh_key.decrypt_private_key(
                ssh_key.private_key
            )

            # Create K8s resources
            v1 = client.CoreV1Api()
            print("creating secret...")
            v1.create_namespaced_secret(
                body=client.V1Secret(
                    metadata=client.V1ObjectMeta(
                        name=name.lower(), namespace=namespace
                    ),
                    string_data=secrets,
                ),
                namespace=namespace,
            )

            k8s_envs = [client.V1EnvVar(name=k, value=v) for k, v in envs.items()]
            k8s_envs.append(client.V1EnvVar(name=HUB_SERVER_ENV, value=SERVER_ADDRESS))
            k8s_envs.append(
                client.V1EnvVar(name=AGENTD_ADDR_ENV, value=desktop_vm.addr),
            )
            k8s_envs.append(
                client.V1EnvVar(
                    name=AGENTSEA_HUB_URL_ENV, value=os.getenv(AGENTSEA_HUB_URL_ENV)
                ),
            )
            k8s_secret_envs = [
                client.V1EnvFromSource(
                    secret_ref=client.V1SecretEnvSource(
                        name=name.lower(), optional=False
                    )
                )
            ]
            print("creating pod...")
            v1.create_namespaced_pod(
                body=client.V1Pod(
                    metadata=client.V1ObjectMeta(
                        name=name.lower(), namespace=namespace
                    ),
                    spec=client.V1PodSpec(
                        containers=[
                            client.V1Container(
                                name="agent",
                                image=agent_type.image,
                                ports=[client.V1ContainerPort(container_port=8080)],
                                env=k8s_envs,
                                env_from=k8s_secret_envs,
                            )
                        ]
                    ),
                ),
                namespace=namespace,
            )
            print("created k8s resources")

            task_agent.status = "created"
            task_agent.save()

            # Wait for the pod to become Running
            if wait_ready:
                print("waiting for pod to become Running...")
                polling_interval = 5
                timeout = 300

                start_time = time.time()
                while True:
                    elapsed_time = time.time() - start_time
                    if elapsed_time > timeout:
                        print("Timeout waiting for pod to become Running.")
                        raise ValueError("Timeout waiting for pod to become Running.")

                    try:
                        pod: client.V1Pod = v1.read_namespaced_pod(
                            name=name, namespace=namespace
                        )
                        status: client.V1PodStatus = pod.status
                        if status.phase == "Running":
                            print("Pod is now running.")
                            break
                        else:
                            print(
                                f"Pod status: {status.phase}. Waiting for Running status..."
                            )
                    except ApiException as e:
                        print(
                            f"Exception when calling CoreV1Api->read_namespaced_pod: {e}"
                        )

                    time.sleep(polling_interval)

        else:
            raise ValueError(f"Unknown provider: {self.provider}")

        if not icon:
            icon = agent_type.icon

        task_agent.secrets = secrets
        task_agent.envs = envs
        task_agent.metadata = metadata
        task_agent.status = "running"
        task_agent.save()
        return task_agent
