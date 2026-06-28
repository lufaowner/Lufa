import socket
import ipaddress
import sys
import os
# languages
LANGS = {
    "1": {"mode_net": "1. Scan network", "mode_ip": "2. Scan IP", "scan": "Scanning...", "open": "OPEN", "closed": "CLOSED", "select": "Select device (1-{}):", "none": "No devices with open ports.", "err": "Invalid selection.", "host": "Host:"},
    "2": {"mode_net": "1. Сканировать сеть", "mode_ip": "2. Сканировать IP", "scan": "Сканирование...", "open": "ОТКРЫТ", "closed": "ЗАКРЫТ", "select": "Выберите устройство (1-{}):", "none": "Нет устройств с открытыми портами.", "err": "Неверный выбор.", "host": "Хост:"},
    "3": {"mode_net": "1. Skanuj sieć", "mode_ip": "2. Skanuj IP", "scan": "Skanowanie...", "open": "OTWARTY", "closed": "ZAMKNIĘTY", "select": "Wybierz urządzenie (1-{}):", "none": "Brak urządzeń z otwartymi portami.", "err": "Błędny wybór.", "host": "Nazwa:"}
}

def banner():
    print(r"""
 _      _    _  _____   ___  
| |    | |  | ||  ___| / _ \ 
| |    | |  | || |__  / /_\ \
| |    | |  | ||  __| |  _  |
| |___ | |__| || |    | | | |
\_____/ \____/ \_|    \_| |_/
""")
    print("OWNER: kartofelek | DC: 84ic")
    print("-" * 40)
# checking ip
def pobierz_hosta(ip):
    try: return socket.gethostbyaddr(ip)[0]
    except: return "Unknown"

def sprawdz_porty(cel, lang):
    porty = [22, 80, 443, 445, 8080]
    wyniki = {}
    for p in porty:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            wyniki[p] = lang['open'] if s.connect_ex((str(cel), p)) == 0 else lang['closed']
            print(f"    Port {p}: {wyniki[p]}")
    return wyniki

def tryb_sieci(lang):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_base = s.getsockname()[0]
    s.close()
    net_range = str(ipaddress.IPv4Network(f"{ip_base}/24", strict=False))
    
    print(f"\n[*] {lang['scan']} {net_range}")
    do_wyboru = []
    
    for ip in ipaddress.IPv4Network(net_range, strict=False):
        if os.system(f"ping -c 1 -W 0.05 {ip} > /dev/null 2>&1") == 0:
            print(f"\n[!] Host: {ip} | {lang['host']} {pobierz_hosta(str(ip))}")
            wyniki = sprawdz_porty(ip, lang)
            if lang['open'] in wyniki.values():
                do_wyboru.append(ip)

    if not do_wyboru:
        print(f"\n[-] {lang['none']}")
    else:
        try:
            print("\n")
            for i, ip in enumerate(do_wyboru, 1): print(f"[{i}] {ip}")
            wybor = input(f"\n{lang['select'].format(len(do_wyboru))} ")
            idx = int(wybor) - 1
            print(f"\n[+] Selected: {do_wyboru[idx]}")
        except: print(f"[-] {lang['err']}")

if __name__ == "__main__":
    banner()
    wybor_l = input("1. English | 2. Русский | 3. Polski\n> ")
    lang = LANGS.get(wybor_l, LANGS["3"])
    
    print(f"\n{lang['mode_net']}\n{lang['mode_ip']}")
    tryb = input("> ")
    
    if tryb == "1":
        tryb_sieci(lang)
    else:
        cel = input("IP: ")
        print(f"\n[*] {lang['scan']} {cel}")
        sprawdz_porty(cel, lang)
