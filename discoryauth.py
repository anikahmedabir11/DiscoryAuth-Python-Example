"""
DiscoryAuth Python SDK
Official Client Library for DiscoryAuth (https://discoryauth.cc)
Supports License Only, User Login, Registration, Cloud Variables & HWID Locking.
"""

import os
import sys
import platform
import subprocess
import requests
import uuid

class UserData:
    def __init__(self, username="", expires_at="", hwid="", license_key="", session_token="", is_lifetime=False):
        self.username = username
        self.expires_at = expires_at
        self.hwid = hwid
        self.license_key = license_key
        self.session_token = session_token
        self.is_lifetime = is_lifetime

class AppData:
    def __init__(self, name="", version="", hwid_lock=True):
        self.name = name
        self.version = version
        self.hwid_lock = hwid_lock

class DiscoryAuth:
    def __init__(self, name: str, app_id: str, secret: str, version: str = "1.0", url: str = "https://discoryauth.cc/api/v1"):
        """
        Initialize DiscoryAuth Client
        :param name: Application name
        :param app_id: Application ID from dashboard (https://discoryauth.cc/app/)
        :param secret: Application Secret Key
        :param version: Client application version (e.g., '1.0')
        :param url: DiscoryAuth API endpoint (default: 'https://discoryauth.cc/api/v1')
        """
        self.name = name
        self.app_id = app_id
        self.secret = secret
        self.version = version
        self.url = url.rstrip('/')
        
        self.session_token = None
        self.initialized = False
        self.hwid = self._get_hwid()
        self.user_data = UserData()
        self.app_data = AppData()

    def _get_hwid(self) -> str:
        """Retrieves a persistent and unique Hardware ID for the machine."""
        try:
            if platform.system() == "Windows":
                # Use Windows MachineGUID from registry
                output = subprocess.check_output(
                    r'wmic csproduct get uuid',
                    shell=True,
                    stderr=subprocess.DEVNULL
                ).decode().split('\n')
                if len(output) > 1 and output[1].strip():
                    return output[1].strip()
        except Exception:
            pass

        # Fallback cross-platform HWID using node hash
        return str(uuid.UUID(int=uuid.getnode())).upper()

    def init(self) -> bool:
        """Initializes application session and checks server status & country maintenance."""
        try:
            payload = {
                "app_id": self.app_id,
                "app_secret": self.secret,
                "hwid": self.hwid,
                "version": self.version
            }
            resp = requests.post(f"{self.url}/init", json=payload, timeout=10)
            data = resp.json()

            if resp.status_code == 200 and data.get("success"):
                self.initialized = True
                app_info = data.get("app", {})
                self.app_data = AppData(
                    name=app_info.get("name", self.name),
                    version=app_info.get("version", self.version),
                    hwid_lock=app_info.get("hwid_lock", True)
                )
                return True
            else:
                msg = data.get("message", "Failed to initialize application.")
                if data.get("code") == "COUNTRY_MAINTENANCE":
                    print(f"[!] Maintenance Alert: {msg}")
                else:
                    print(f"[-] Init Error: {msg}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"[-] Network Connection Error: {e}")
            return False

    def check_initialized(self):
        if not self.initialized:
            raise RuntimeError("Please call api.init() before attempting authentication.")

    def license(self, license_key: str) -> bool:
        """Authenticates using License Key only (KeyAuth Key-Only mode)."""
        self.check_initialized()
        try:
            payload = {
                "app_id": self.app_id,
                "app_secret": self.secret,
                "license_key": license_key.strip(),
                "hwid": self.hwid
            }
            resp = requests.post(f"{self.url}/license", json=payload, timeout=10)
            data = resp.json()

            if resp.status_code == 200 and data.get("success"):
                u = data.get("user", {})
                self.session_token = data.get("session_token")
                self.user_data = UserData(
                    username=u.get("username", "DiscoryUser"),
                    expires_at=u.get("expires_at", "Never"),
                    hwid=u.get("hwid", self.hwid),
                    license_key=u.get("license_key", license_key),
                    session_token=self.session_token,
                    is_lifetime=u.get("is_lifetime", False)
                )
                return True
            else:
                print(f"[-] License Error: {data.get('message', 'Invalid license key.')}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"[-] Network Error: {e}")
            return False

    def login(self, username: str, password: str) -> bool:
        """Authenticates an existing user with username and password."""
        self.check_initialized()
        try:
            payload = {
                "app_id": self.app_id,
                "app_secret": self.secret,
                "username": username.strip(),
                "password": password.strip(),
                "hwid": self.hwid
            }
            resp = requests.post(f"{self.url}/login", json=payload, timeout=10)
            data = resp.json()

            if resp.status_code == 200 and data.get("success"):
                u = data.get("user", {})
                self.session_token = data.get("session_token")
                self.user_data = UserData(
                    username=u.get("username", username),
                    expires_at=u.get("expires_at", "Never"),
                    hwid=u.get("hwid", self.hwid),
                    license_key=u.get("license_key", ""),
                    session_token=self.session_token
                )
                return True
            else:
                print(f"[-] Login Error: {data.get('message', 'Login failed.')}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"[-] Network Error: {e}")
            return False

    def register(self, username: str, password: str, license_key: str) -> bool:
        """Registers a new user account linked with a license key."""
        self.check_initialized()
        try:
            payload = {
                "app_id": self.app_id,
                "app_secret": self.secret,
                "username": username.strip(),
                "password": password.strip(),
                "license_key": license_key.strip(),
                "hwid": self.hwid
            }
            resp = requests.post(f"{self.url}/register", json=payload, timeout=10)
            data = resp.json()

            if resp.status_code == 200 and data.get("success"):
                u = data.get("user", {})
                self.user_data = UserData(
                    username=u.get("username", username),
                    expires_at=u.get("expires_at", "Never")
                )
                return True
            else:
                print(f"[-] Registration Error: {data.get('message', 'Registration failed.')}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"[-] Network Error: {e}")
            return False

    def var(self, var_id_or_name: str) -> str:
        """Retrieves a secure cloud variable defined on the developer dashboard."""
        self.check_initialized()
        try:
            payload = {
                "app_id": self.app_id,
                "app_secret": self.secret,
                "var_id": var_id_or_name,
                "session_token": self.session_token
            }
            resp = requests.post(f"{self.url}/var", json=payload, timeout=10)
            data = resp.json()
            if data.get("success"):
                return data.get("response", "")
            return ""
        except Exception:
            return ""

    def check(self) -> bool:
        """Verifies if the current user session is valid and active."""
        if not self.session_token:
            return False
        try:
            payload = {
                "app_id": self.app_id,
                "app_secret": self.secret,
                "session_token": self.session_token
            }
            resp = requests.post(f"{self.url}/check", json=payload, timeout=5)
            data = resp.json()
            return bool(data.get("success"))
        except Exception:
            return False

    def log(self, message: str):
        """Sends an audit log entry to the developer dashboard."""
        try:
            payload = {
                "app_id": self.app_id,
                "app_secret": self.secret,
                "message": message,
                "pcuser": os.getenv("USERNAME", "PythonUser")
            }
            requests.post(f"{self.url}/log", json=payload, timeout=5)
        except Exception:
            pass
