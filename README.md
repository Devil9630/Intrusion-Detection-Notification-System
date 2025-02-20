# 🛡️ Intrusion Detection & Notification System

![Status](https://img.shields.io/badge/Status-Active-brightgreen) ![Python](https://img.shields.io/badge/Made%20with-Python-blue) ![Security](https://img.shields.io/badge/Security-Critical-red)

## 🌟 Overview
A real-time security tool that detects unauthorized IP scanning attempts on a network. This tool continuously monitors incoming traffic, identifies reconnaissance activities, and instantly notifies administrators via SMS alerts, helping prevent potential cyber threats.

## 🚀 Key Features
- ✅ **Real-time Detection**: Identifies network reconnaissance and port scanning attempts.
- 📩 **Instant Notifications**: Sends automated SMS alerts with the attacker's IP address.
- ⚙️ **Customizable Rules**: Modify detection settings to minimize false positives.
- 🔄 **Seamless Integration**: Works with existing security monitoring systems.

## 🏗️ Technologies Used
- **Python** 🐍
- **Scapy** 📡 (for network traffic analysis)
- **Twilio API** 📲 (for SMS notifications)
- **IPTables** 🔥 (for traffic filtering)
- **Linux Scripting** 🖥️ (for automation)

## 🎯 How It Works
1. Monitors network traffic in real time.
2. Detects suspicious IP scanning activities.
3. Sends an SMS alert with the attacker's IP for immediate response.

## 📦 Installation
```bash
# Clone the repository
git clone https://github.com/your-username/intrusion-detection-system.git
cd intrusion-detection-system

# Install dependencies
pip install -r requirements.txt
```

## 🔧 Usage
```bash
python detect.py --interface eth0 --threshold 10
```
Options:
- `--interface` : Network interface to monitor.
- `--threshold` : Number of requests per second to trigger detection.

## 📧 SMS Alerts
Configure Twilio API settings in `config.py` to receive SMS notifications.

## 🏆 Contributing
We welcome contributions! Feel free to submit issues or pull requests.

## 📝 License
This project is licensed under the MIT License.

## 🤝 Connect
💼 LinkedIn: linkedin.com/in/er-mehul-dubey
