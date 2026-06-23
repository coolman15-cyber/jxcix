import os
import socket
import hashlib
import secrets
import string
import subprocess
import ssl
import datetime
import time
import random
import uuid
import base64
import platform
import getpass
import json

APP_NAME = "JXCIX TOOLS"
LOG_DIR = "logs"
CONFIG_FILE = "jxcix_config.json"

try:
    import psutil
except ImportError:
    psutil = None

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import track
    from rich.text import Text
    from rich.align import Align
    from rich.columns import Columns
    from rich import box
    RICH = True
except ImportError:
    RICH = False
    Console = None

console = Console() if RICH else None


DEFAULT_CONFIG = {
    "accent": "dark_red",
    "boot_animation": True,
    "show_dashboard": True
}


THEMES = {
    "dark_red": {
        "accent": "red",
        "accent2": "bright_red",
        "ok": "green",
        "warn": "yellow",
        "text": "white",
        "muted": "grey70",
        "border": "red"
    },
    "cyan": {
        "accent": "cyan",
        "accent2": "bright_cyan",
        "ok": "green",
        "warn": "yellow",
        "text": "white",
        "muted": "grey70",
        "border": "cyan"
    },
    "green": {
        "accent": "green",
        "accent2": "bright_green",
        "ok": "green",
        "warn": "yellow",
        "text": "white",
        "muted": "grey70",
        "border": "green"
    }
}


def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        cfg = DEFAULT_CONFIG.copy()
        cfg.update(data)
        return cfg
    except Exception:
        return DEFAULT_CONFIG.copy()


def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4)


CONFIG = load_config()


def theme():
    return THEMES.get(CONFIG.get("accent", "dark_red"), THEMES["dark_red"])


def styled(text, style=None):
    if RICH:
        return f"[{style or theme()['text']}]{text}[/{style or theme()['text']}]"
    return text


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress Enter to continue...")


def log(text):
    os.makedirs(LOG_DIR, exist_ok=True)
    filename = datetime.datetime.now().strftime(f"{LOG_DIR}/log_%Y-%m-%d.txt")
    now = datetime.datetime.now().strftime("%H:%M:%S")
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"[{now}] {text}\n")


def printx(text="", style=None):
    if RICH:
        console.print(text, style=style)
    else:
        print(text)


def run_cmd(cmd):
    try:
        subprocess.run(cmd, shell=False)
    except Exception as e:
        print(f"[!] Command error: {e}")


def logo_text():
    return r"""
      ██╗██╗  ██╗ ██████╗██╗██╗  ██╗
      ██║╚██╗██╔╝██╔════╝██║╚██╗██╔╝
      ██║ ╚███╔╝ ██║     ██║ ╚███╔╝
 ██   ██║ ██╔██╗ ██║     ██║ ██╔██╗
 ╚█████╔╝██╔╝ ██╗╚██████╗██║██╔╝ ██╗
  ╚════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝╚═╝  ╚═╝
"""


def logo():
    if RICH:
        return Text(logo_text(), style=f"bold {theme()['accent']}")
    return logo_text()


def boot_screen():
    if not CONFIG.get("boot_animation", True):
        return

    clear()
    if RICH:
        console.print(Align.center(logo()))
        console.print(Align.center(f"[bold {theme()['accent2']}]{APP_NAME}[/bold {theme()['accent2']}]"))
        console.print(Align.center("[white]Legal Cybersecurity Toolkit[/white]\n"))
    else:
        print(logo_text())
        print(APP_NAME)
        print("Legal Cybersecurity Toolkit\n")

    steps = [
        "Initializing core",
        "Loading network tools",
        "Loading file tools",
        "Loading system dashboard",
        "Checking local environment",
        "Starting toolkit"
    ]

    if RICH:
        for step in steps:
            console.print(f"[{theme()['accent']}]>[/] {step}...", end="")
            time.sleep(random.uniform(0.08, 0.22))
            console.print(f" [{theme()['ok']}]OK[/]")
        for _ in track(range(25), description=f"[{theme()['accent']}]Loading[/]"):
            time.sleep(0.015)
        console.print(f"\n[bold {theme()['ok']}]ACCESS GRANTED[/bold {theme()['ok']}]")
        console.print(f"[{theme()['accent2']}]Welcome, {getpass.getuser()}[/]")
    else:
        for step in steps:
            print(f"[+] {step}... OK")
            time.sleep(0.15)
        print("\nACCESS GRANTED")
        print(f"Welcome, {getpass.getuser()}")

    time.sleep(0.9)


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "Unknown"


def today_log_count():
    filename = datetime.datetime.now().strftime(f"{LOG_DIR}/log_%Y-%m-%d.txt")
    if not os.path.exists(filename):
        return 0
    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
        return len(f.readlines())


def dashboard_panels():
    user = getpass.getuser()
    os_name = f"{platform.system()} {platform.release()}"
    now = datetime.datetime.now().strftime("%H:%M:%S")
    date = datetime.datetime.now().strftime("%d.%m.%Y")

    if psutil:
        cpu = f"{psutil.cpu_percent(interval=0.15)}%"
        ram = f"{psutil.virtual_memory().percent}%"
        disk = f"{psutil.disk_usage('/').percent}%"
    else:
        cpu = ram = disk = "N/A"

    border = theme()["border"]

    panels = [
        Panel(
            f"CPU  : {cpu}\nRAM  : {ram}\nDisk : {disk}",
            title="SYSTEM",
            border_style=border,
            box=box.ROUNDED
        ),
        Panel(
            f"User : {user}\nOS   : {os_name}\nTime : {now}\nDate : {date}",
            title="LOCAL",
            border_style=border,
            box=box.ROUNDED
        ),
        Panel(
            f"Status : Connected\nHost   : {platform.node()}\nIP     : {get_local_ip()}",
            title="NETWORK",
            border_style=border,
            box=box.ROUNDED
        ),
        Panel(
            f"Today logs : {today_log_count()}\nFolder     : {LOG_DIR}\\",
            title="LOGS",
            border_style=border,
            box=box.ROUNDED
        ),
    ]
    return panels


def banner():
    clear()

    if RICH:
        console.print(Align.center(logo()))
        console.print(Align.center(f"[bold {theme()['accent2']}]{APP_NAME}[/bold {theme()['accent2']}]"))
        console.print(Align.center("[white]Legal Cybersecurity Toolkit[/white]\n"))

        if CONFIG.get("show_dashboard", True):
            console.print(Columns(dashboard_panels(), equal=True, expand=True))

        console.print(Panel(f"[bold {theme()['ok']}]Status: READY[/bold {theme()['ok']}]", border_style=theme()["border"]))
    else:
        print(logo_text())
        print("=" * 55)
        print(f"{APP_NAME:^55}")
        print("Legal Cybersecurity Toolkit".center(55))
        print("=" * 55)


def menu():
    if not RICH:
        print("""
[ NETWORK ]
[1] Ping host
[2] DNS lookup
[3] Safe port scanner
[4] SSL certificate checker
[5] Show network connections

[ FILES ]
[6] File hash checker
[7] Find duplicate files

[ UTILS ]
[8] Strong password generator
[9] Random username
[10] UUID generator
[11] Base64 encoder
[12] Base64 decoder

[ SYSTEM ]
[13] PC information
[14] System dashboard
[15] Running processes
[16] Startup programs
[17] Windows audit
[18] Cleanup tips

[ LOGS ]
[20] View today's logs
[21] Open logs folder

[ SETTINGS ]
[30] Settings

[0] Exit
""")
        return

    table = Table(show_header=True, header_style=f"bold {theme()['accent2']}", box=box.ROUNDED, expand=True)
    table.add_column("NETWORK", style="white")
    table.add_column("FILES", style="white")
    table.add_column("UTILS", style="white")
    table.add_column("SYSTEM", style="white")
    table.add_column("LOGS", style="white")

    rows = [
        ("[1] Ping host", "[6] File hash checker", "[8] Strong password", "[13] PC information", "[20] View today's logs"),
        ("[2] DNS lookup", "[7] Find duplicates", "[9] Random username", "[14] System dashboard", "[21] Open logs folder"),
        ("[3] Safe port scanner", "", "[10] UUID generator", "[15] Running processes", ""),
        ("[4] SSL certificate", "", "[11] Base64 encoder", "[16] Startup programs", ""),
        ("[5] Connections", "", "[12] Base64 decoder", "[17] Windows audit", ""),
        ("", "", "", "[18] Cleanup tips", ""),
    ]

    for row in rows:
        table.add_row(*row)

    console.print(table)
    console.print(Panel("[30] Settings     [0] Exit", border_style=theme()["border"]))


def ping_host():
    host = input("Host/IP: ").strip()
    run_cmd(["ping", "-n", "4", host])
    log(f"PING {host}")


def dns_lookup():
    domain = input("Domain: ").strip()
    try:
        ip = socket.gethostbyname(domain)
        print(f"[+] {domain} -> {ip}")
        log(f"DNS {domain} -> {ip}")
    except Exception as e:
        print(f"[!] Error: {e}")


def port_scan():
    print("Scan only your own devices or systems you have permission to test.")
    host = input("Host/IP: ").strip()
    ports = input("Ports example 22,80,443: ").strip()

    for p in ports.split(","):
        try:
            port = int(p.strip())
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.7)
            result = sock.connect_ex((host, port))
            sock.close()

            status = "OPEN" if result == 0 else "CLOSED"
            print(f"[{status}] {host}:{port}")
            log(f"PORT {status} {host}:{port}")
        except Exception:
            print(f"[!] Invalid port: {p}")


def ssl_checker():
    domain = input("Domain example google.com: ").strip()
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(5)
            s.connect((domain, 443))
            cert = s.getpeercert()

        print("Issuer:", cert.get("issuer"))
        print("Valid from:", cert.get("notBefore"))
        print("Valid until:", cert.get("notAfter"))
        log(f"SSL CHECK {domain}")
    except Exception as e:
        print(f"[!] SSL error: {e}")


def network_connections():
    run_cmd(["netstat", "-ano"])
    log("NETSTAT")


def file_hash():
    path = input("File path: ").strip().replace('"', "")
    if not os.path.exists(path):
        print("[!] File not found")
        return

    sha256 = hashlib.sha256()
    md5 = hashlib.md5()

    with open(path, "rb") as f:
        for block in iter(lambda: f.read(8192), b""):
            sha256.update(block)
            md5.update(block)

    print("SHA256:", sha256.hexdigest())
    print("MD5:   ", md5.hexdigest())
    log(f"HASH {path}")


def find_duplicates():
    folder = input("Folder path: ").strip().replace('"', "")
    if not os.path.isdir(folder):
        print("[!] Folder not found")
        return

    print("[*] Scanning files...")
    hashes = {}
    duplicates = []

    for root, _, files in os.walk(folder):
        for name in files:
            path = os.path.join(root, name)
            try:
                h = hashlib.sha256()
                with open(path, "rb") as f:
                    for block in iter(lambda: f.read(8192), b""):
                        h.update(block)
                digest = h.hexdigest()

                if digest in hashes:
                    duplicates.append((path, hashes[digest]))
                else:
                    hashes[digest] = path
            except Exception:
                pass

    if not duplicates:
        print("[+] No duplicates found.")
    else:
        print("[!] Duplicates found:")
        for dup, original in duplicates:
            print("\nDuplicate:", dup)
            print("Original :", original)

    log(f"DUPLICATE SCAN {folder}")


def password_gen():
    try:
        length = int(input("Password length: "))
        if length < 8:
            print("[!] Minimum length is 8")
            return
    except Exception:
        print("[!] Wrong number")
        return

    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}"
    password = "".join(secrets.choice(chars) for _ in range(length))
    print("Password:", password)
    log("PASSWORD GENERATED")


def random_username():
    words = ["shadow", "cyber", "zero", "nova", "byte", "ghost", "matrix", "echo", "neon", "root", "jxcix"]
    name = secrets.choice(words) + "_" + secrets.choice(words) + str(secrets.randbelow(9999))
    print("Username:", name)
    log("USERNAME GENERATED")


def uuid_generator():
    value = str(uuid.uuid4())
    print("UUID:", value)
    log("UUID GENERATED")


def b64_encode():
    text = input("Text to encode: ")
    encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")
    print("Base64:", encoded)
    log("BASE64 ENCODE")


def b64_decode():
    text = input("Base64 to decode: ")
    try:
        decoded = base64.b64decode(text.encode("utf-8")).decode("utf-8")
        print("Decoded:", decoded)
        log("BASE64 DECODE")
    except Exception:
        print("[!] Invalid Base64")


def pc_info():
    print("[ SYSTEM INFO ]\n")
    print("User       :", getpass.getuser())
    print("Computer   :", platform.node())
    print("OS         :", platform.platform())
    print("Python     :", platform.python_version())
    print("Local IP   :", get_local_ip())

    if psutil:
        print("CPU Usage  :", psutil.cpu_percent(interval=1), "%")
        print("RAM Usage  :", psutil.virtual_memory().percent, "%")
        print("Disk Usage :", psutil.disk_usage("/").percent, "%")
        print("\nNetwork Interfaces:")
        for nic in psutil.net_if_addrs():
            print(" -", nic)
    else:
        print("\nInstall psutil for CPU/RAM/Disk info:")
        print("python -m pip install psutil")

    log("PC INFO")


def system_dashboard():
    if not psutil:
        print("Install psutil first: python -m pip install psutil")
        return

    try:
        while True:
            clear()
            print("JXCIX SYSTEM DASHBOARD\n")
            print("CPU :", psutil.cpu_percent(interval=0.5), "%")
            print("RAM :", psutil.virtual_memory().percent, "%")
            print("Disk:", psutil.disk_usage("/").percent, "%")
            print("\nPress CTRL + C to return.")
            time.sleep(0.8)
    except KeyboardInterrupt:
        pass

    log("SYSTEM DASHBOARD")


def running_processes():
    if not psutil:
        print("Install psutil first: python -m pip install psutil")
        return

    print("PID       NAME")
    print("-" * 40)
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            print(f"{proc.info['pid']:<9} {proc.info['name']}")
        except Exception:
            pass

    log("RUNNING PROCESSES")


def startup_programs():
    print("Startup programs from Windows registry:")
    run_cmd(["reg", "query", r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run"])
    print()
    run_cmd(["reg", "query", r"HKLM\Software\Microsoft\Windows\CurrentVersion\Run"])
    log("STARTUP PROGRAMS")


def windows_audit():
    print("[1] System info")
    print("[2] Users")
    print("[3] Firewall status")
    choice = input("Select: ").strip()

    if choice == "1":
        run_cmd(["systeminfo"])
    elif choice == "2":
        run_cmd(["net", "user"])
    elif choice == "3":
        run_cmd(["netsh", "advfirewall", "show", "allprofiles"])
    else:
        print("[!] Wrong option")

    log("WINDOWS AUDIT")


def cleanup_tips():
    print("""
Safe cleanup tips:

1. Open Disk Cleanup:
   cleanmgr

2. Open temporary folder:
   %TEMP%

3. Check large folders manually before deleting.

4. Do not delete Windows/System32 files.

5. Create a restore point before big cleanup.
""")
    log("CLEANUP TIPS")


def view_today_logs():
    filename = datetime.datetime.now().strftime(f"{LOG_DIR}/log_%Y-%m-%d.txt")
    if not os.path.exists(filename):
        print("[!] No logs today.")
        return

    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
        print(f.read())


def open_logs_folder():
    os.makedirs(LOG_DIR, exist_ok=True)
    os.startfile(LOG_DIR)


def settings_menu():
    global CONFIG
    print("""
[ SETTINGS ]

[1] Accent: dark_red
[2] Accent: cyan
[3] Accent: green
[4] Toggle boot animation
[5] Toggle dashboard
[0] Back
""")
    choice = input("Select: ").strip()

    if choice == "1":
        CONFIG["accent"] = "dark_red"
    elif choice == "2":
        CONFIG["accent"] = "cyan"
    elif choice == "3":
        CONFIG["accent"] = "green"
    elif choice == "4":
        CONFIG["boot_animation"] = not CONFIG.get("boot_animation", True)
    elif choice == "5":
        CONFIG["show_dashboard"] = not CONFIG.get("show_dashboard", True)
    elif choice == "0":
        return
    else:
        print("[!] Wrong option")
        return

    save_config(CONFIG)
    print("[+] Settings saved.")


def main():
    actions = {
        "1": ping_host,
        "2": dns_lookup,
        "3": port_scan,
        "4": ssl_checker,
        "5": network_connections,
        "6": file_hash,
        "7": find_duplicates,
        "8": password_gen,
        "9": random_username,
        "10": uuid_generator,
        "11": b64_encode,
        "12": b64_decode,
        "13": pc_info,
        "14": system_dashboard,
        "15": running_processes,
        "16": startup_programs,
        "17": windows_audit,
        "18": cleanup_tips,
        "20": view_today_logs,
        "21": open_logs_folder,
        "30": settings_menu,
    }

    while True:
        banner()
        menu()
        choice = input("jxcix> ").strip()

        if choice == "0":
            print("Bye, jxcix.")
            break

        clear()

        if RICH:
            console.print(Align.center(f"[bold {theme()['accent2']}]{APP_NAME}[/bold {theme()['accent2']}]\n"))
        else:
            print(APP_NAME + "\n")

        action = actions.get(choice)
        if action:
            action()
        else:
            print("[!] Wrong option")

        pause()


if __name__ == "__main__":
    boot_screen()
    main()
