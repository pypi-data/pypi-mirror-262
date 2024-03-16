from typing import List, Annotated
import asyncio

import asyncssh
from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    WebSocket,
    WebSocketDisconnect,
    APIRouter,
)
import asyncssh
from agentdesk import Desktop

from guisurfer.server.models import V1UserProfile
from guisurfer.auth.transport import get_current_user
from guisurfer.server.key import SSHKeyPair

router = APIRouter()


async def ssh_proxy(
    websocket: WebSocket,
    host: str,
    username: str,
    private_ssh_key: str,
    port: int = 6080,
):
    # Connect to the SSH server using the private key for authentication
    async with asyncssh.connect(
        host,
        port=port,
        username=username,
        client_keys=[asyncssh.import_private_key(private_ssh_key)],
    ) as conn:
        # Open a direct TCP/IP channel to the destination (WebSocket service)
        async with conn.open_connection("localhost", 6080) as ssh_conn:
            try:
                await websocket.accept()
                while True:
                    # Wait for data from either the WebSocket or the SSH connection
                    tasks = [
                        asyncio.create_task(websocket.receive_text()),
                        asyncio.create_task(ssh_conn.reader.read(65536)),
                    ]
                    done, pending = await asyncio.wait(
                        tasks, return_when=asyncio.FIRST_COMPLETED
                    )

                    # Relay data received from the WebSocket to the SSH connection
                    for task in done:
                        if task == tasks[0]:  # Data received from WebSocket
                            data = task.result()
                            ssh_conn.writer.write(data.encode())
                            await ssh_conn.writer.drain()
                        else:  # Data received from SSH connection
                            data = task.result()
                            await websocket.send_text(data.decode())

                    for task in pending:
                        task.cancel()

            except WebSocketDisconnect:
                print("WebSocket disconnected")
            except Exception as e:
                print(f"Error: {e}")


@router.websocket("/ws/vnc/{desktop_name}")
async def websocket_proxy(
    websocket: WebSocket,
    current_user: Annotated[V1UserProfile, Depends(get_current_user)],
    desktop_name: str,
):
    found = Desktop.find(owner_id=current_user.email, name=desktop_name)
    if len(found) == 0:
        raise HTTPException(status_code=404, detail=f"Desktop {desktop_name} not found")
    desktop = found[0]

    found = SSHKeyPair.find(owner_id=current_user.email, public_key=desktop.ssh_key)
    if len(found) == 0:
        raise HTTPException(
            status_code=404, detail=f"SSH key for desktop {desktop_name} not found"
        )

    key_pair = found[0]
    private_key = key_pair.decrypt_private_key(key_pair.private_key)

    # Proxy the WebSocket connection to the SSH connection
    await ssh_proxy(
        websocket, desktop.addr, username="agentsea", ssh_private_key=private_key
    )
