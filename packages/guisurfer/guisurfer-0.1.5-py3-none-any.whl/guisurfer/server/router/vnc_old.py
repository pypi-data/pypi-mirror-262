import asyncssh


async def ssh_proxy_old(
    websocket: WebSocket,
    host: str,
    username: str,
    private_ssh_key: str,
    ws_port: int = 6080,
    ssh_port: int = 22,
    headers: Dict[str, str] = {},
):
    print("WS establishing ssh connection...")
    print("WS host: ", host)
    print("WS ssh_port: ", ssh_port)
    print("WS ws_port: ", ws_port)
    print("WS username: ", username)

    try:
        conn = await asyncssh.connect(
            host,
            port=ssh_port,
            username=username,
            client_keys=[asyncssh.import_private_key(private_ssh_key)],
            known_hosts=None,
        )
        print("WS SSH connection established.")

        opened = await conn.open_connection("localhost", ws_port)
        print("opened: ", opened)
        print("type opened: ", type(opened))
        reader, writer = opened
        print("WS Direct TCP/IP channel opened.")

        print("WS connecting to websocket with headers: ", headers)
        await websocket.accept(headers=headers)
        print("WS WebSocket accepted.")
        ping_task = asyncio.create_task(ping_websocket(websocket, 5, 10))

        while True:
            print("WS Starting proxy while loop.")
            ws_task = asyncio.create_task(websocket.receive_text())
            ssh_task = asyncio.create_task(reader.read(65536))
            tasks = [ws_task, ssh_task, ping_task]
            print("WS Created tasks.")

            done, pending = await asyncio.wait(
                tasks, return_when=asyncio.FIRST_COMPLETED
            )
            print("WS Completed waiting for tasks.")

            for task in done:
                if task == ws_task:
                    try:
                        data = task.result()
                        print("WS Received data from WebSocket: ", data)
                        writer.write(data.encode())
                        await writer.drain()
                        print("WS Sent data to SSH.")
                    except WebSocketDisconnect:
                        print("WS WebSocket disconnected.")
                        break
                elif task == ssh_task:
                    data = task.result()
                    print("WS Received data from SSH: ", data)
                    await websocket.send_text(data.decode())
                    print("WS Sent data to WebSocket.")

            for task in pending:
                task.cancel()
                print("WS Cancelled pending task.")

    except asyncio.exceptions.IncompleteReadError:
        print("WS Incomplete read from WebSocket. Closing connection.")
        await websocket.close()
    except asyncssh.ConnectionLost as e:
        print(f"WS SSH ConnectionLost: {e}")
    except WebSocketDisconnect:
        print("WS WebSocket disconnected.")
    except Exception as e:
        print(f"WS Async Error: {e}")
        raise
    finally:
        if writer:
            writer.close()
            await writer.wait_closed()
        print("WS SSH connection closed.")
        await conn.close()
        print("WS SSH connection closed gracefully.")


async def ping_websocket(websocket: WebSocket, interval: int, timeout: int):
    while True:
        try:
            await asyncio.sleep(interval)
            await websocket.send_bytes(b"ping")
            print("WS Sent ping.")
            pong = await asyncio.wait_for(websocket.receive_bytes(), timeout=timeout)
            if pong == b"pong":
                print("WS Received pong.")
            else:
                print("WS Received unexpected message instead of pong.")
        except asyncio.TimeoutError:
            print("WS Ping timeout. Closing connection.")
            await websocket.close()
            break
        except WebSocketDisconnect:
            print("WS WebSocket disconnected during ping.")
            break
        except Exception as e:
            print(f"WS Ping error: {e}")
            break
