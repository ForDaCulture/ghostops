# handlers/http.py
# Fake HTTP service handler for HoneyGuard honeypot.
# Logs each HTTP request (request line + headers + body) and responds with a 404 page.

import asyncio
from honeyguard.logger import log_event

# Simple HTML 404 response
HTTP_404_BODY = b"""
<html>
  <head><title>404 Not Found</title></head>
  <body><h1>Not Found</h1><p>The requested URL was not found on this server.</p></body>
</html>
"""
HTTP_404_RESPONSE = (
    b"HTTP/1.1 404 Not Found\r\n"
    b"Content-Type: text/html; charset=UTF-8\r\n"
    b"Content-Length: " + str(len(HTTP_404_BODY)).encode() + b"\r\n"
    b"Connection: close\r\n"
    b"\r\n"
) + HTTP_404_BODY

async def handle_http(reader: asyncio.StreamReader,
                      writer: asyncio.StreamWriter,
                      src_ip: str,
                      port: int):
    """
    1. Read the HTTP request line and headers until CRLF CRLF.
    2. Log the raw request.
    3. Send a fixed 404 Not Found response.
    4. Log the response event and close.
    """
    try:
        # 1. Read until we see the end of headers
        raw_request = b""
        while True:
            line = await reader.readline()
            if not line or line == b"\r\n":
                # End of headers
                raw_request += line
                break
            raw_request += line

        # Decode for logging (ignore errors)
        text_request = raw_request.decode(errors="ignore")

        # 2. Log the HTTP request event
        await log_event({
            'event': 'http_request',
            'src_ip': src_ip,
            'port': port,
            'request': text_request,
        })

        # 3. Send the 404 response
        writer.write(HTTP_404_RESPONSE)
        await writer.drain()

        # 4. Log that we sent a response
        await log_event({
            'event': 'http_response',
            'src_ip': src_ip,
            'port': port,
            'status': 404,
        })

    except Exception as e:
        # Log any errors during HTTP handling
        await log_event({
            'event': 'http_error',
            'src_ip': src_ip,
            'port': port,
            'error': str(e),
        })

    finally:
        writer.close()
        await writer.wait_closed()
