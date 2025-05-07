# handlers/ssh.py
# Fake SSH service handler for HoneyGuard honeypot.
# Sends a synthetic SSH banner, logs incoming data, and then closes.

import asyncio
from honeyguard.logger import log_event

# A realistic SSH banner (pretend version)
SSH_BANNER = "SSH-2.0-OpenSSH_7.4p1 Ubuntu-10\r\n"

# Timeout for read attempts (in seconds)
READ_TIMEOUT = 5

async def handle_ssh(reader: asyncio.StreamReader,
                     writer: asyncio.StreamWriter,
                     src_ip: str,
                     port: int):
    """
    Emulate an SSH service:
      1. Send a fake SSH banner.
      2. Loop reading incoming data until timeout.
      3. Log each data chunk as an event.
      4. Close connection.
    """
    # Send the SSH banner
    writer.write(SSH_BANNER.encode())
    await writer.drain()

    await log_event({
        'event': 'ssh_banner_sent',
        'src_ip': src_ip,
        'port': port,
        'banner': SSH_BANNER.strip(),
        'timestamp': asyncio.get_event_loop().time()
    })

    # Continuously read input until client disconnects or timeout
    while True:
        try:
            # Wait for up to READ_TIMEOUT seconds for data
            data = await asyncio.wait_for(reader.read(1024), timeout=READ_TIMEOUT)
            if not data:
                # No data = client closed connection
                break

            # Decode and strip control chars
            text = data.decode(errors='ignore').strip()

            # Log what the attacker typed
            await log_event({
                'event': 'ssh_input',
                'src_ip': src_ip,
                'port': port,
                'input': text,
                'timestamp': asyncio.get_event_loop().time()
            })

            # Optionally, send a fake "authentication failed" message for realism
            writer.write(b"Permission denied, please try again.\r\n")
            await writer.drain()

        except asyncio.TimeoutError:
            # No data for READ_TIMEOUT seconds → assume done
            break
        except Exception as e:
            # Log unexpected errors
            await log_event({
                'event': 'ssh_error',
                'src_ip': src_ip,
                'port': port,
                'error': str(e),
                'timestamp': asyncio.get_event_loop().time()
            })
            break

    # Close the connection
    writer.close()
    await writer.wait_closed()

    await log_event({
        'event': 'ssh_connection_closed',
        'src_ip': src_ip,
        'port': port,
        'timestamp': asyncio.get_event_loop().time()
    })
