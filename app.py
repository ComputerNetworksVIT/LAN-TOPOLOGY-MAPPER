# app.py
from flask import Flask, jsonify, send_from_directory
from scanner import scan_network
import json, os

app = Flask(__name__, static_folder='static')

def compare_scans(old_scan, new_scan):
    old_macs = {d['mac']: d for d in old_scan.get('devices', []) if d.get('mac') and d['mac'] != "Unknown"}
    new_macs = {d['mac']: d for d in new_scan.get('devices', []) if d.get('mac') and d['mac'] != "Unknown"}

    joined = [v for k, v in new_macs.items() if k not in old_macs]
    left = [v for k, v in old_macs.items() if k not in new_macs]
    same = [v for k, v in new_macs.items() if k in old_macs]

    return {"joined": joined, "left": left, "same": same}

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/scan')
def api_scan():
    s = scan_network()
    return jsonify(s)

@app.route('/api/devices')
def api_devices():
    if os.path.exists("last_scan.json"):
        with open("last_scan.json") as f:
            return jsonify(json.load(f))
    return jsonify({"devices": []})

@app.route('/api/compare')
def api_compare():
    if not os.path.exists("last_scan.json"):
        old_scan = {"devices": []}
    else:
        with open("last_scan.json") as f:
            old_scan = json.load(f)

    new_scan = scan_network()
    diff = compare_scans(old_scan, new_scan)
    with open("last_scan.json", "w") as f:
        json.dump(new_scan, f, indent=2)
    return jsonify(diff)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5055, debug=True)