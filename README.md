# DiscoryAuth-Python-Example : Please star ⭐

DiscoryAuth Python example SDK for [https://discoryauth.cc](https://discoryauth.cc) license key & user authentication API.

This example allows you to securely license and protect your Python software against piracy with hardware locking, expiry tracking, remote cloud variables, and audit logging.

---

### Features
* **Key-Only Authentication**: Let users login directly with just their license key.
* **Username & Password Authentication**: Complete registration and login system.
* **Hardware ID (HWID) Lock**: Automatically locks keys to user machines.
* **Country Maintenance Bypassing**: Instant cloud alerts when maintenance is triggered.
* **Cloud Variables**: Dynamically deliver sensitive secrets and configs from your server.
* **Dashboard Audit Logs**: Monitor who enters your app in real-time.

---

### Installation & Setup

1. **Clone or Download this repository**
2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure your Application credentials in `main.py`:**
   Head to your developer dashboard on [discoryauth.cc](https://discoryauth.cc/app/) and copy your credentials:
   ```python
   APP_NAME    = "My Protected App"
   APP_ID      = "app_xxxxxxxx"
   APP_SECRET  = "sec_xxxxxxxxxxxxxxxxxxxx"
   APP_VERSION = "1.0"
   API_URL     = "https://discoryauth.cc/api/v1"
   ```
4. **Run the example:**
   ```bash
   python main.py
   ```

---

### License
This project is open-source under the MIT License.
