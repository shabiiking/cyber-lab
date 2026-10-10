
from flask import Flask, jsonify, send_from_directory
import psutil
import platform
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__, static_folder=None)

START_TIME = time.time()


@app.get("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/style.css")
def stylesheet():
    return send_from_directory(BASE_DIR, "style.css")


@app.get("/script.js")
def javascript():
    return send_from_directory(BASE_DIR, "script.js")


@app.get("/api/status")
def system_status():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    # Use a short non-blocking CPU sample.
    cpu_percent = psutil.cpu_percent(interval=None)

    return jsonify({
        "cpu_percent": cpu_percent,
        "ram_percent": memory.percent,
        "ram_used_gb": round(memory.used / (1024 ** 3), 2),
        "ram_total_gb": round(memory.total / (1024 ** 3), 2),
        "disk_percent": disk.percent,
        "disk_used_gb": round(disk.used / (1024 ** 3), 1),
        "disk_total_gb": round(disk.total / (1024 ** 3), 1),
        "uptime_seconds": int(time.time() - psutil.boot_time()),
        "platform": platform.system(),
        "hostname": platform.node()
    })


if __name__ == "__main__":
    # Accessible only from this laptop.
    app.run(host="127.0.0.1", port=5000, debug=False)

