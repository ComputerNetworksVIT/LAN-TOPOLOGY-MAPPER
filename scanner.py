'''# scanner.py
import socket
import time
import json
from manuf import manuf
import nmap

def guess_local_subnet():
    return "192.168.29.0/24"   # <- update if your subnet changes

def scan_network(subnet=None, arguments='-PR -sn -T4'):
    if subnet is None:
        subnet = guess_local_subnet()

    nm = nmap.PortScanner()
    nm.scan(hosts=subnet, arguments=arguments)
    mf = manuf.MacParser()
    devices = []

    for host in nm.all_hosts():
        st = nm[host].get('status', {}).get('state', 'unknown')
        if st != 'up':
            continue

        addr = nm[host].get('addresses', {})
        ip = addr.get('ipv4') or host
        mac = addr.get('mac') or "Unknown"

        vendor = "Unknown"
        if mac and mac != "Unknown":
            try:
                vendor = mf.get_manuf(mac) or "Unknown"
            except Exception:
                vendor = "Unknown"

        hostname = None
        hostnames = nm[host].get('hostnames', [])
        if hostnames:
            for h in hostnames:
                name = h.get('name')
                if name:
                    hostname = name
                    break

        if not hostname:
            try:
                fqdn = socket.getfqdn(ip)
                if fqdn and fqdn != ip:
                    hostname = fqdn
            except Exception:
                hostname = None

        devices.append({
            "ip": ip,
            "mac": mac,
            "vendor": vendor,
            "hostname": hostname or "Unknown",
            "state": st
        })

    snapshot = {"timestamp": time.time(), "subnet": subnet, "devices": devices}
    with open("last_scan.json", "w") as f:
        json.dump(snapshot, f, indent=2)
    return snapshot

if __name__ == "__main__":
    print(json.dumps(scan_network(), indent=2))'''

'''import scapy.all as scapy
import json
import os
import time
from manuf import manuf  # for vendor lookup

# Initialize vendor lookup
manuf_lookup = manuf.MacParser()

def is_alive(ip):
    """Ping the IP to confirm it’s actually alive."""
    response = os.system(f"ping -c 1 -W 1 {ip} > /dev/null 2>&1")
    return response == 0  # 0 = alive

def scan_network(subnet):
    """Scan the given subnet for connected devices."""
    print(f"Scanning network: {subnet} ...")
    arp_request = scapy.ARP(pdst=subnet)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]

    devices = []

    for element in answered_list:
        ip = element[1].psrc
        mac = element[1].hwsrc

        # Ping check – only include if it's actually reachable
        if not is_alive(ip):
            continue

        vendor = manuf_lookup.get_manuf(mac)
        devices.append({
            "ip": ip,
            "mac": mac,
            "vendor": vendor if vendor else "Unknown"
        })

    result = {
        "timestamp": time.time(),
        "subnet": subnet,
        "devices": devices
    }

    # Save results as JSON
    with open("scan_results.json", "w") as f:
        json.dump(result, f, indent=4)

    return result

# Example subnet – change if needed
if __name__ == "__main__":
    subnet = "192.168.29.0/24"  # Adjust based on your hotspot’s network
    print(json.dumps(scan_network(subnet), indent=4)) '''


'''import nmap
import json
import time
from manuf import manuf

def scan_network(subnet):
    print(f"Scanning network: {subnet} ...")

    nm = nmap.PortScanner()
    nm.scan(hosts=subnet, arguments='-sn')  # -sn means ping scan (no ports)

    manuf_lookup = manuf.MacParser()
    devices = []

    for host in nm.all_hosts():
        if 'mac' in nm[host]['addresses']:
            mac = nm[host]['addresses']['mac']
            vendor = manuf_lookup.get_manuf(mac)
        else:
            mac = 'Unknown'
            vendor = 'Unknown'

        devices.append({
            'ip': host,
            'mac': mac,
            'vendor': vendor
        })

    result = {
        'timestamp': time.time(),
        'subnet': subnet,
        'devices': devices
    }

    with open('scan_results.json', 'w') as f:
        json.dump(result, f, indent=4)

    return result

if __name__ == "__main__":
    subnet = "192.168.29.0/24"  # replace if needed
    print(json.dumps(scan_network(subnet), indent=4))'''

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