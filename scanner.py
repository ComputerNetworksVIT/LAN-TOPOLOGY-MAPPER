import subprocess
import json
import re
import time
import ipaddress
import socket

def get_local_subnet():
    try:
        # Detect local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()

        # Assume /24 subnet (works for most hotspots & routers)
        subnet = str(ipaddress.ip_network(local_ip + "/24", strict=False))
        return subnet
    except Exception as e:
        print("Error detecting local subnet:", e)
        return "192.168.29.0/24"

def scan_network():
    subnet = get_local_subnet()
    print(f"🔍 Scanning network: {subnet} ...")

    # Run nmap scan — only show live hosts with MAC
    cmd = ["sudo", "nmap", "-sn", subnet]
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout

    # Parse output
    devices = []
    current_ip = None
    for line in output.splitlines():
        if "Nmap scan report for" in line:
            match = re.search(r"Nmap scan report for (.+)", line)
            if match:
                current_ip = match.group(1).strip()
        elif "MAC Address" in line:
            match = re.search(r"MAC Address: ([0-9A-F:]+) \((.*?)\)", line)
            if match and current_ip:
                mac = match.group(1)
                vendor = match.group(2)
                devices.append({
                    "ip": current_ip,
                    "mac": mac,
                    "vendor": vendor
                })
                current_ip = None  # reset for next device

    # Remove duplicates
    unique_devices = {d["mac"]: d for d in devices}.values()

    data = {
        "timestamp": time.time(),
        "subnet": subnet,
        "devices": list(unique_devices)
    }
    print(json.dumps(data, indent=4))
    return data

if __name__ == "__main__":
    scan_network()