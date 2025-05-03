import http.server
import ssl

PORT = 443
CERT = "cert.pem"
KEY = "key.pem"

handler = http.server.SimpleHTTPRequestHandler
httpd = http.server.HTTPServer(("0.0.0.0", PORT), handler)

httpd.socket = ssl.wrap_socket(httpd.socket, keyfile=KEY, certfile=CERT, server_side=True)

print(f"[+] HTTPS server running on port {PORT}")
httpd.serve_forever()
