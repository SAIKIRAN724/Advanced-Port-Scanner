# Advanced Port Scanner with Visualization

An advanced Python-based port scanning tool that goes beyond traditional port scanners by providing
service banner grabbing, stealth scanning, scan speed control, statistical analysis, and visual reporting.

---

## 🚀 Features

- Multi-threaded TCP port scanning
- Banner grabbing for service identification
- Stealth scan mode for low-noise scanning
- User-controlled scan speed (rate limiting)
- Open vs Closed port percentage analysis
- Pie chart visualization using Matplotlib
- Export scan results in TXT, CSV, or JSON format
- User-defined output file path

---

## 🛠️ Tools & Technologies Used

- **Python**
- **socket** – network communication
- **threading** – concurrent port scanning
- **time & datetime** – scan timing and rate control
- **matplotlib** – visualization (pie chart)
- **json & csv** – structured data export

---

## 🧠 Project Architecture

The scanner sends TCP connection requests to the target system through the network.
Based on the response, ports are classified as open or closed.
For open ports, service banners are collected.
Results are analyzed, visualized, and saved in a user-defined format.

---

## ▶️ How to Run the Project

```bash```
pip install matplotlib
python scanner.py

Follow the on-screen prompts to enter:
Target IP / domain
Port range
Scan speed
Stealth mode option
Output file path

📊 Output
Console-based scan results
Pie chart showing open vs closed port percentage
Saved scan report file (TXT / CSV / JSON)

⚠️ Disclaimer
This tool is developed strictly for educational and ethical security testing purposes.
Do NOT scan systems without proper authorization.

