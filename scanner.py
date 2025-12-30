import socket
import threading
import time
from datetime import datetime
import json
import csv
import matplotlib.pyplot as plt

print("🛠️ Advanced Port Scanner (Python)\n")

# -------------------- USER INPUT --------------------
target = input("Enter IP address or domain: ")
start_port = int(input("Enter start port: "))
end_port = int(input("Enter end port: "))
save_path = input("Enter output file path (txt / csv / json): ")
rate_limit = int(input("Enter scan rate (1-10, 1 = slowest): "))
is_stealth = input("Enable stealth scan (Y/N): ").lower() == 'y'

# -------------------- START TIME --------------------
start_time = datetime.now()

# -------------------- HOST RESOLUTION --------------------
try:
    ip = socket.gethostbyname(target)
    hostname = socket.gethostbyaddr(ip)[0]
    print(f"\n🎯 Target Resolved: {target} ({ip}) | Hostname: {hostname}")
except socket.gaierror:
    print("❌ Invalid IP or Domain")
    exit()

print(f"\n🔍 Scanning ports {start_port} to {end_port}...\n")

open_ports = []
results = []
lock = threading.Lock()

# -------------------- BANNER GRABBING --------------------
def grab_banner(sock):
    try:
        sock.send(b'HEAD / HTTP/1.1\r\n\r\n')
        return sock.recv(1024).decode(errors="ignore").strip()
    except:
        return "No banner"

# -------------------- STEALTH SCAN --------------------
def stealth_scan(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect_ex((ip, port))
        s.close()
    except:
        pass

# -------------------- PORT SCAN --------------------
def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)

        if is_stealth:
            stealth_scan(port)
            return

        result = s.connect_ex((ip, port))
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown"

            banner = grab_banner(s)

            with lock:
                msg = f"Port {port} OPEN ({service}) | {banner}"
                print("✅", msg)
                open_ports.append(port)
                results.append(msg)

        s.close()
    except:
        pass

# -------------------- RATE CONTROL --------------------
def rate_control():
    time.sleep(1 / rate_limit)

# -------------------- THREADING --------------------
threads = []
for port in range(start_port, end_port + 1):
    t = threading.Thread(target=scan_port, args=(port,))
    threads.append(t)
    t.start()
    rate_control()

for t in threads:
    t.join()

# -------------------- END TIME --------------------
end_time = datetime.now()
duration = (end_time - start_time).total_seconds()

# -------------------- SUMMARY --------------------
total_ports = end_port - start_port + 1
open_count = len(open_ports)
closed_count = total_ports - open_count

print("\n✅ Scan Completed")
print(f"⏱️ Duration: {duration:.2f} seconds")
print(f"📊 Open Ports: {open_count}")
print(f"📊 Closed Ports: {closed_count}")

# -------------------- PIE CHART --------------------
labels = ["Open Ports", "Closed Ports"]
sizes = [open_count, closed_count]
colors = ["green", "red"]
explode = (0.1, 0)

plt.figure(figsize=(6, 6))
plt.pie(
    sizes,
    labels=labels,
    colors=colors,
    autopct="%1.1f%%",
    startangle=140,
    explode=explode,
    shadow=True
)
plt.title(f"Port Status Distribution for {target}")
plt.axis("equal")
plt.show()

# -------------------- SAVE RESULTS --------------------
ext = save_path.split(".")[-1].lower()

if ext == "txt":
    with open(save_path, "w") as f:
        f.write(f"Target: {target} ({ip})\n")
        f.write(f"Ports Scanned: {start_port}-{end_port}\n\n")
        for r in results:
            f.write(r + "\n")
        f.write(f"\nDuration: {duration:.2f} seconds\n")

elif ext == "csv":
    with open(save_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Port", "Service", "Banner"])
        for r in results:
            parts = r.split("|")
            port = parts[0].split()[1]
            service = parts[0].split("(")[1].split(")")[0]
            banner = parts[1].strip()
            writer.writerow([port, service, banner])

elif ext == "json":
    data = {
        "target": target,
        "ip": ip,
        "scan_range": f"{start_port}-{end_port}",
        "duration": duration,
        "open_ports": results
    }
    with open(save_path, "w") as f:
        json.dump(data, f, indent=4)

print(f"\n📁 Results saved to {save_path}")
