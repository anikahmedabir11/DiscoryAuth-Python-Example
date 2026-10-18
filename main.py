"""
DiscoryAuth Python Example Application
Demonstrates KeyAuth-style Authentication with DiscoryAuth (https://discoryauth.cc)
"""

import sys
import time
from discoryauth import DiscoryAuth

# ==============================================================================
# DISCORyAUTH CONFIGURATION
# Obtain credentials from your DiscoryAuth Developer Dashboard: https://discoryauth.cc/app/
# ==============================================================================
APP_NAME    = "My Protected App"
APP_ID      = "app_xxxxxxxx"               # Replace with your Application ID
APP_SECRET  = "sec_xxxxxxxxxxxxxxxxxxxx"   # Replace with your Application Secret
APP_VERSION = "1.0"
API_URL     = "https://discoryauth.cc/api/v1" # Or "http://localhost:8080/api/v1" for local testing

def print_banner():
    banner = r"""
  ____  _                               _         _   _     
 |  _ \(_)___  ___ ___  _ __ _   _     / \  _   _| |_| |__  
 | | | | / __|/ __/ _ \| '__| | | |   / _ \| | | | __| '_ \ 
 | |_| | \__ \ (_| (_) | |  | |_| |  / ___ \ |_| | |_| | | |
 |____/|_|___/\___\___/|_|   \__, | /_/   \_\__,_|\__|_| |_|
                             |___/                          
    :: Official Python Example | https://discoryauth.cc ::
"""
    print(banner)

def main():
    print_banner()

    # Initialize DiscoryAuth Client
    print("[*] Connecting to DiscoryAuth Network...")
    auth = DiscoryAuth(
        name=APP_NAME,
        app_id=APP_ID,
        secret=APP_SECRET,
        version=APP_VERSION,
        url=API_URL
    )

    if not auth.init():
        print("[-] Initialization failed! Please check your credentials or internet connection.")
        input("\nPress Enter to exit...")
        sys.exit(1)

    print(f"[+] Initialized application: {auth.app_data.name} (v{auth.app_data.version})")
    print(f"[+] Hardware ID: {auth.hwid}\n")

    print("Select an option:")
    print(" [1] Login")
    print(" [2] Register")
    print(" [3] License Key Only")
    print(" [4] Exit")

    choice = input("\nChoice > ").strip()

    if choice == "1":
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        print("[*] Verifying credentials...")
        if auth.login(username, password):
            print(f"\n[+] Successfully logged in as: {auth.user_data.username}")
        else:
            input("\nPress Enter to exit...")
            sys.exit(1)

    elif choice == "2":
        username = input("Enter new Username: ").strip()
        password = input("Enter new Password: ").strip()
        key = input("Enter License Key: ").strip()
        print("[*] Registering account...")
        if auth.register(username, password, key):
            print("\n[+] Registration complete! You can now log in.")
        else:
            input("\nPress Enter to exit...")
            sys.exit(1)

    elif choice == "3":
        key = input("Enter License Key: ").strip()
        print("[*] Authenticating license key...")
        if auth.license(key):
            print(f"\n[+] License Key Accepted! Welcome {auth.user_data.username}!")
        else:
            input("\nPress Enter to exit...")
            sys.exit(1)

    elif choice == "4":
        sys.exit(0)
    else:
        print("[-] Invalid choice.")
        sys.exit(1)

    # --------------------------------------------------------------------------
    # POST-AUTHENTICATION SECTION
    # The user has now authenticated successfully!
    # --------------------------------------------------------------------------
    print("\n" + "="*50)
    print("           USER DASHBOARD / PROFILE")
    print("="*50)
    print(f" Username     : {auth.user_data.username}")
    print(f" Expires At   : {auth.user_data.expires_at}")
    print(f" Hardware ID  : {auth.user_data.hwid}")
    print(f" License Key  : {auth.user_data.license_key or 'N/A'}")
    print("="*50)

    # Fetching a Cloud Variable (Defined in your dashboard under Variables)
    print("\n[*] Fetching remote variable 'secret_config'...")
    config_data = auth.var("secret_config")
    if config_data:
        print(f"[+] Variable Data: {config_data}")
    else:
        print("[-] Variable 'secret_config' not set or empty.")

    # Sending an audit log to your DiscoryAuth developer dashboard
    auth.log(f"User {auth.user_data.username} launched the application successfully.")

    print("\n[+] Heartbeat Check: Session is valid!")
    print("[*] Running protected application payload...")
    print("[*] Everything secure. Enjoy your software!\n")

    input("Press Enter to exit application...")

if __name__ == "__main__":
    main()
