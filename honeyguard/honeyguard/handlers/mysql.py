# handlers/mysql.py
# Fake MySQL service handler for HoneyGuard honeypot.
# Sends a minimal handshake, reads client's auth packet, logs it, then closes.

import asyncio
from honeyguard.logger import log_event

# Minimal MySQL handshake packet (protocol v10, server version string, thread id, scramble, etc.)
# NOTE: This is a dummy byte sequence to trigger client auth.
MYSQL_HANDSHAKE = bytes.fromhex(
    "0a352e362e3335002d68756e6b65722d706f742d7373696d"+  # "5.6.35-hunker-pot-ssim"
    "0000000100000000" +                                 # thread id + filler
    "0000000000000000" +                                 # scramble placeholder
    "ff"                                                 # end
)

async def handle_mysql(reader: asyncio.StreamReader,
                       writer: asyncio.StreamWriter,
                       src_ip: str,
                       port: int):
    """
    1. Send a fake MySQL handshake packet.
    2. Read client's auth packet (up to 4096 bytes).
    3. Log the raw auth packet as hex.
    4. Close the connection.
    """
    try:
        # 1. Deliver handshake
        writer.write(MYSQL_HANDSHAKE)
        await writer.drain()
        await log_event({
            'event': 'mysql_handshake_sent',
            'src_ip': src_ip,
            'port': port,
        })

        # 2. Await the client's auth packet (blocking up to 5s)
        auth_data = await asyncio.wait_for(reader.read(4096), timeout=5)
        if auth_data:
            # 3. Log the auth packet as hex string
            await log_event({
                'event': 'mysql_auth_packet',
                'src_ip': src_ip,
                'port': port,
                'auth_hex': auth_data.hex(),
            })

    except asyncio.TimeoutError:
        # No auth packet received
        await log_event({
            'event': 'mysql_timeout',
            'src_ip': src_ip,
            'port': port,
        })
    except Exception as e:
        # Any other error
        await log_event({
            'event': 'mysql_error',
            'src_ip': src_ip,
            'port': port,
            'error': str(e),
        })
    finally:
        writer.close()
        await writer.wait_closed()
        await log_event({
            'event': 'mysql_connection_closed',
            'src_ip': src_ip,
            'port': port,
        })
