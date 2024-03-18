from typing import List, Annotated, Dict
import asyncio
import traceback
import time

from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    WebSocket,
    WebSocketDisconnect,
    APIRouter,
    Query,
)
import asyncssh
from agentdesk import Desktop
from starlette.datastructures import Headers as StarletteHeaders
import websockets
from websockets import WebSocketClientProtocol
from agentdesk.util import find_open_port
from agentdesk.proxy import ensure_ssh_proxy, cleanup_proxy

from guisurfer.server.models import V1UserProfile
from guisurfer.auth.transport import get_current_user
from guisurfer.server.key import SSHKeyPair

router = APIRouter()


async def handle_client(websocket: WebSocket, ws: WebSocketClientProtocol):
    try:
        while True:
            # Receive binary data from the client
            print(f"\nWS waiting for binary data from client...")
            data = await websocket.receive_bytes()
            print(f"\nWS Received binary data from client")
            # Send binary data to the websockify service
            await ws.send(data)
    except Exception as e:
        print(f"WS Error handling client binary data: {e}, Type: {type(e).__name__}")
        print(f"Stack trace: {traceback.format_exc()}")


async def handle_websockify(websocket: WebSocket, ws: WebSocketClientProtocol):
    try:
        while True:
            # Receive binary data from the websockify service
            print(f"\nWS waiting for binary data from server...")
            data = await ws.recv()
            print(f"\nWS Received binary data from websockify")
            # Send binary data to the client
            await websocket.send_bytes(data)
    except Exception as e:
        print(f"\n WS Error handling websockify binary data: {e}")


async def ssh_proxy(
    websocket: WebSocket,
    host: str,
    username: str,
    private_ssh_key: str,
    ws_port: int = 6080,
    ssh_port: int = 22,
    headers: Dict[str, str] = {},
):

    reconnect_delay = 1
    try:
        print("WS establishing ssh connection...")
        print("WS host: ", host)
        print("WS ssh_port: ", ssh_port)
        local_port = find_open_port(6000, 8000)
        print("WS local_port: ", local_port)
        pid = ensure_ssh_proxy(
            local_port=local_port,
            remote_port=ws_port,
            ssh_host=host,
            ssh_key=private_ssh_key,
        )
        time.sleep(2)
        print("WS ssh_proxy started.")

        # TODO: pass headers?
        async with websockets.connect(f"ws://127.0.0.1:{local_port}") as ws:
            print("WS WebSocket connected.")
            while True:
                try:
                    client_task = asyncio.create_task(handle_client(websocket, ws))
                    websockify_task = asyncio.create_task(
                        handle_websockify(websocket, ws)
                    )
                    await asyncio.gather(client_task, websockify_task)

                except asyncio.TimeoutError:
                    # Handle timeout if no data is received from websockify
                    print("WS timeout error")
                    pass
                except websockets.exceptions.ConnectionClosed:
                    # Handle connection closure
                    print("WS connection closed")
                    break
                except Exception as e:
                    print(f"WS Error: {e}")
                    raise

    except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed) as e:
        print(f"WS Connection closed or timed out: {e}")
        # reconnect_attempts += 1
        print(f"WS Reconnecting in {reconnect_delay} seconds... (Attempting...)")
        await asyncio.sleep(reconnect_delay)
        reconnect_delay = min(reconnect_delay * 2, 60)
    except asyncio.exceptions.IncompleteReadError:
        print("WS Incomplete read from WebSocket. Closing connection.")
        await websocket.close()
    except WebSocketDisconnect:
        print("WS WebSocket disconnected.")
    except Exception as e:
        print(f"WS Async Error: {e}")
        raise
    finally:
        try:
            cleanup_proxy(pid)
        except Exception as e:
            print(f"WS Cleanup error: {e}")


@router.websocket("/ws/vnc/{desktop_name}")
async def websocket_proxy(
    websocket: WebSocket,
    desktop_name: str,
    token: str = Query(...),
):
    try:
        current_user = await get_current_user(token)
        print("\nWS current_user: ", current_user)
        print("\nWS finding desktop: ", desktop_name)
        found = Desktop.find(owner_id=current_user.email, name=desktop_name.lower())
        if len(found) == 0:
            raise HTTPException(
                status_code=404, detail=f"Desktop {desktop_name} not found"
            )
        desktop = found[0]
        print("\nWS found desktop")

        print("\nWS finding key pair")
        found = SSHKeyPair.find(owner_id=current_user.email, public_key=desktop.ssh_key)
        if len(found) == 0:
            raise HTTPException(
                status_code=404, detail=f"SSH key for desktop {desktop_name} not found"
            )

        key_pair = found[0]
        print("\nWS found key pair")
        private_key = key_pair.decrypt_private_key(key_pair.private_key)
        # print("\nWS using private key: ", private_key)

        await websocket.accept()
    except Exception as e:
        print(f"WS Error: {e}")
        raise

    print("\nWS starting ssh proxy")
    # Proxy the WebSocket connection to the SSH connection
    send_headers = _filter_and_adjust_headers(websocket.headers, desktop.addr)

    try:
        await ssh_proxy(
            websocket=websocket,
            host=desktop.addr,
            username="agentsea",
            private_ssh_key=private_key,
            headers=send_headers,
        )
    except Exception as e:
        print(f"\nWS proxy Error: {e}")
        raise


def _filter_and_adjust_headers(headers: StarletteHeaders, addr: str) -> List[tuple]:
    filtered_headers = []
    for key, value in headers.items():
        key_lower = key.lower()
        if key_lower in [
            "sec-websocket-key",
            "sec-websocket-version",
            "sec-websocket-extensions",
            "cookie",
            "authorization",
        ]:
            continue
        if key_lower == "host":
            value = addr
        filtered_headers.append((key.encode("latin1"), value.encode("latin1")))
    return filtered_headers
