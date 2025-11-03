# LAN-TOPOLOGY-MAPPER
Amritha.D.B (24BCE5064) Mokshita.C.V(24BCE1094) Smrithi.S(24BCE1698)

## Overview

The **Wi-Fi Network Scanner** is a Python-based project built using **Flask**, **Scapy**, and **Nmap** to detect all active devices connected to a local network (LAN or Wi-Fi hotspot).  

It displays key details such as:
- Device **IP address**
- **MAC address**
- **Vendor/Manufacturer** name
- **Network Topology Visualization** – shows how devices are connected within the local network.

This tool demonstrates practical **network discovery**, **packet-level scanning**, and **web-based visualization** concepts — ideal for cybersecurity, IoT, and computer networks coursework.

---

## Features

- 🔍 **Real-time device scanning** within your network  
- 🌐 **Web interface** built using Flask  
- 🧠 **Automatic subnet detection** (e.g., 192.168.0.0/24)  
- 🧭 **Topology Visualization** of connected devices  
- ⚙️ **Combines Nmap & ARP scanning** for high accuracy  
- 💻 **Cross-platform compatibility** (macOS, Windows, Linux)  

---

##  File Structure

```
wifi-scanner/
│
├── app.py                # Flask backend server
├── scanner.py            # Network scanning logic (Nmap + ARP)
├── static/
│   ├── index.html        # Web interface for scanning & viewing devices
└── README.md             # Project documentation
```

---

## Working Principle

1. The user accesses the **web interface** served by Flask.  
2. When “**Scan Network**” is clicked, the browser sends a request to `/api/scan`.  
3. `scanner.py`:
   - Detects your **subnet**  
   - Runs **Nmap** and **ARP requests** to find connected devices  
   - Retrieves IP, MAC, and Vendor details  
   - Returns the data to Flask for rendering in the UI  
4. The result is shown dynamically on the web page — including a **graphical network topology** of all connected devices.

---

## Setup Instructions (macOS Version)

### 1. Clone or copy the project folder
Ensure the folder structure looks like this:
```
wifi-scanner/
│── app.py
│── scanner.py
│── static/
│   ├── index.html
```

### 2. Create a virtual environment
```bash
cd wifi-scanner
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install flask scapy python-nmap
```

### 4. Run the Flask server
```bash
sudo python3 app.py
```
(`sudo` is required for network scanning permissions)

If you get:
> Port 5055 already in use  
Run:
```bash
sudo lsof -i :5055
sudo kill -9 <PID>
sudo python3 app.py
```

### 5️⃣ Access in your browser
```
http://127.0.0.1:5055
```
or from another device on the same network:
```
http://<your_mac_ip>:5055
```

---

## 📶 Using a Mobile Hotspot (Important)

If scanning via a **mobile hotspot**, ensure all devices are in the **same local network**.  
Many hotspots **isolate devices**, preventing detection. Follow one of the setups below 👇

---

### ✅ **Option A (Recommended)** — Use Mac as a Router (Internet Sharing)

1. Go to **System Settings → General → Sharing**  
2. Enable **Internet Sharing**  
3. Share your connection **from:** Wi-Fi / iPhone USB  
4. Share **to computers using:** Wi-Fi  
5. Click **Wi-Fi Options** → set:
   - Network Name: `MyMacHotspot`  
   - Security: `WPA2 Personal`  
   - Password: `12345678`
6. Turn ON **Internet Sharing**  
7. Connect your phone/laptop to this hotspot  
8. Run the scanner again — devices will now be discoverable 🎯  

---

### ✅ **Option B** — Use a Mobile Hotspot (Phone as Router)

1. Connect **Mac + other devices** to the **same hotspot**  
2. Disable network privacy filters:
   - **On iPhone:**  
     *Settings → Wi-Fi → (i)* → turn off *Private Wi-Fi Address* and *Limit IP Tracking*
   - **On Mac:**  
     *System Settings → Network → Wi-Fi → (i)* → disable *Limit IP Address Tracking*
3. Click **Renew DHCP Lease** on your Mac’s Wi-Fi settings.  
4. Find your Mac’s IP:
   ```bash
   ipconfig getifaddr en0
   ```
5. Run:
   ```bash
   sudo python3 app.py
   ```
6. Open in browser:
   ```
   http://127.0.0.1:5055
   ```
   or
   ```
   http://<your_mac_ip>:5055
   ```

> Some mobile hotspots block LAN discovery — if scan results are empty, switch to Option A.

---

## Troubleshooting

| Issue | Cause | Fix |
|--------|--------|-----|
| No devices found | Mobile hotspot isolation | Use Internet Sharing mode |
| Port 5055 busy | Flask instance still running | `sudo lsof -i :5055` → `sudo kill -9 <PID>` |
| Permission denied | Missing sudo | Run `sudo python3 app.py` |
| Vendor shows as "Unknown" | Vendor DB incomplete | Update Nmap or add manually |

