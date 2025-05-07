# ghostops_honeyguard/server.py
# Asyncio-based honeypot server that listens on multiple ports
# and dispatches incoming connections to appropriate service handlers.

import asyncio
from honeyguard.handlers.ssh import handle_ssh
from honeyguard.handlers.http import handle_http
from honeyguard.handlers.mysql import handle_mysql
from honeyguard.logger import log_event

# 1. Map ports to handler functions
#    Each handler implements a fake service (SSH, HTTP, MySQL)
PORT_HANDLERS = {
    22: handle_ssh,
    80: handle_http,
    443: handle_http,
    3306: handle_mysql,
}

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, port: int):
    """
    Entry point for each client connection.
    - reader: stream to read incoming bytes
    - writer: stream to write responses
    - port: the port on which this connection was accepted
    """
    peername = writer.get_extra_info('peername')
    src_ip = peername[0]

    # 2. Log the start of the connection event
    await log_event({
        'event': 'connection_start',
        'src_ip': src_ip,
        'port': port,
        'timestamp': asyncio.get_event_loop().time()
    })

    # 3. Dispatch to the protocol-specific handler
    handler = PORT_HANDLERS.get(port)
    if handler:
        # Handler runs the fake protocol session
        await handler(reader, writer, src_ip, port)
    else:
        # No handler available: just close the connection
        writer.close()
        await writer.wait_closed()

    # 4. Log the end of the connection event
    await log_event({
        'event': 'connection_end',
        'src_ip': src_ip,
        'port': port,
        'timestamp': asyncio.get_event_loop().time()
    })

async def start_honeypot():
    """
    Spin up an asyncio TCP server on each port defined in PORT_HANDLERS.
    Each server will run handle_client for every incoming connection.
    """
    tasks = []
    loop = asyncio.get_event_loop()

    for port in PORT_HANDLERS:
        # Create a server on 0.0.0.0:<port>
        server = await asyncio.start_server(
            lambda r, w, p=port: handle_client(r, w, p),
            host='0.0.0.0',
            port=port
        )
        print(f"[+] HoneyGuard listening on port {port}")
        # Schedule the server to run indefinitely
        tasks.append(server.serve_forever())

    # Run all servers in parallel until the program is terminated
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    # Entry point: start the honeypot event loop
    try:
        asyncio.run(start_honeypot())
    except KeyboardInterrupt:
        print("\n[!] Shutting down HoneyGuard...")
