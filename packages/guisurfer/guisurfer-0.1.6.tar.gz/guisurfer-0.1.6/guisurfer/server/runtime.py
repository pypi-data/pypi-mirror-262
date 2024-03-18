import base64
import os
from cryptography.fernet import Fernet
from dataclasses import dataclass, field
from typing import List, Optional, Dict
import uuid
import time
import json

from agentdesk.vm import DesktopVM
from agentdesk.vm.ec2 import EC2Provider
from agentdesk.vm.gce import GCEProvider

from guisurfer.db.conn import WithDB
from guisurfer.db.models import DesktopRuntimeRecord, AgentRuntimeRecord
from .models import (
    DesktopRuntimeModel,
    AgentRuntimeModel,
    GCEProviderOptions,
    EC2ProviderOptions,
)
from .key import SSHKeyPair


@dataclass
class DesktopRuntime(WithDB):
    """A runtime for desktop vms"""

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

    def to_record(self) -> DesktopRuntimeRecord:
        metadata_ = json.dumps(self.metadata) if self.metadata else None
        return DesktopRuntimeRecord(
            id=self.id,
            owner_id=self.owner_id,
            name=self.name,
            provider=self.provider,
            credentials=self.credentials,
            created=self.created,
            updated=self.updated,
            metadata_=metadata_,
            full_name=f"{self.owner_id}/{self.name}",
        )

    @classmethod
    def from_record(cls, record: DesktopRuntimeRecord) -> "DesktopRuntime":
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

    def to_schema(self) -> DesktopRuntimeModel:
        return DesktopRuntimeModel(
            id=self.id,
            name=self.name,
            provider=self.provider,
            created=self.created,
            updated=self.updated,
            metadata=self.metadata if self.metadata else {},
        )

    def save(self) -> None:
        for db in self.get_db():
            db.add(self.to_record())
            db.commit()

    @classmethod
    def find(cls, **kwargs) -> List["DesktopRuntime"]:
        for db in cls.get_db():
            records = db.query(DesktopRuntimeRecord).filter_by(**kwargs).all()
            return [cls.from_record(record) for record in records]

    @classmethod
    def delete(cls, name: str, owner_id: str) -> None:
        for db in cls.get_db():
            record = (
                db.query(DesktopRuntimeRecord)
                .filter_by(name=name, owner_id=owner_id)
                .first()
            )
            if record:
                db.delete(record)
                db.commit()

    def create(
        self,
        ssh_key_name: Optional[str] = None,
        gce_opts: Optional[GCEProviderOptions] = None,
        ec2_opts: Optional[EC2ProviderOptions] = None,
        name: Optional[str] = None,
        image: Optional[str] = None,
        memory: int = 4,
        cpu: int = 2,
        disk: str = "30gb",
        tags: Optional[Dict[str, str]] = None,
        reserve_ip: bool = False,
        owner_id: Optional[str] = None,
    ) -> DesktopVM:
        creds = self.decrypt_credentials(self.credentials)
        if self.provider == "gce":
            if not gce_opts:
                raise ValueError("GCE options required")

            key = creds["GOOGLE_APPLICATION_CREDENTIALS_JSON"]
            service_account_info = json.loads(key)
            project_id = service_account_info.get("project_id")
            if not project_id:
                raise ValueError("project_id not found in credentials")
            provider = GCEProvider(
                project_id=project_id,
                zone=gce_opts.zone,
                region=gce_opts.region,
                gcp_credentials_json=key,
            )

        elif self.provider == "ec2":
            if not ec2_opts:
                raise ValueError("EC2 options required")

            provider = EC2Provider(
                region=ec2_opts.region,
                aws_access_key_id=creds[0]["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=creds[0]["AWS_SECRET_ACCESS_KEY"],
            )

        else:
            raise ValueError("Invalid provider")

        if ssh_key_name:
            print("finding ssh key pair")
            key = SSHKeyPair.find(name=ssh_key_name, owner_id=owner_id)
            if not key:
                raise ValueError("SSH key not found")

        else:
            print("generating ssh key pair")
            key = SSHKeyPair.find(name=name, owner_id=owner_id)
            if not key:
                key = SSHKeyPair.generate_key(
                    name=name, owner_id=owner_id, metadata={"generated_for": name}
                )
            else:
                if key[0].metadata.get("generated_for") != name:
                    # TODO: this is funny
                    raise ValueError(
                        f"SSH key found with name '{name}' but is not tied to this desktop"
                    )

        print("\ncreating vm with keys:")
        print("\nprivate key: \n", key.decrypt_private_key(key.private_key))
        print("\npublic key: \n", key.public_key)

        vm = provider.create(
            name=name.lower(),
            memory=memory,
            image=image,
            cpu=cpu,
            disk=disk,
            tags=tags,
            reserve_ip=reserve_ip,
            public_ssh_key=key.public_key,
            private_ssh_key=key.decrypt_private_key(key.private_key),
            owner_id=owner_id,
        )

        print("\npast provider create")

        return vm
