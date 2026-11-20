import os
import re
import ssl
import json
import socket
import hashlib
import secrets
import string
import platform
import uuid
import ipaddress
import base64

from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime

R = "\033[91m"
G = "\033[92m"
Y = "\033[93m"
B = "\033[94m"
C = "\033[96m"
M = "\033[95m"
W = "\033[97m"
X = "\033[0m"


def line():
    print(C + "=" * 48 + X)


def ok(msg):
    print(G + "[+] " + str(msg) + X)


def warn(msg):
    print(Y + "[!] " + str(msg) + X)


def fail(msg):
    print(R + "[-] " + str(msg) + X)


def ask(msg):
    return input(C + msg + X).strip()


def pause():
    input(Y + "\nPress ENTER to continue..." + X)


def title():
    os.system("clear")
    print(R + r"""
 ██████╗██╗   ██╗██████╗ ███████╗██████╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝
██║       ╚██╔╝  ██╔══██╗██╔══██╗██╔══██╗
╚██████╗   ██║   ██████╔╝███████╗██║  ██║
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝
""" + X)

    print(C + r"""
██╗     ██╗ ██████╗ ███╗   ██╗
██║     ██║██╔═══██╗████╗  ██║
██║     ██║██║   ██║██╔██╗ ██║
██║     ██║██║   ██║██║╚██╗██║
███████╗██║╚██████╔╝██║ ╚████║
╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
""" + X)

    line()
    print(M + "       ULTIMATE SECURITY TOOLKIT" + X)
    print(Y + "       VERSION 3.0 | 30 MODULES" + X)
    print(G + "       CREATED BY GOKU" + X)
    print(G + "       [ SYSTEM ONLINE ]" + X)
    line()


# 01 - URL Analyzer
def url_analyzer():
    u = ask("Enter URL: ")
    try:
        p = urlparse(u)

        if p.scheme not in ("http", "https") or not p.hostname:
            raise ValueError("Invalid URL")

        ok("Domain: " + p.hostname)
        print("Protocol:", p.scheme)
        print("Port:", p.port or "Default")
        print("Path:", p.path or "/")
        print("HTTPS:", p.scheme == "https")
        print("Embedded credentials:", bool(p.username or p.password))

    except ValueError as e:
        fail(e)


# 02 - HTTPS Checker
def https_checker():
    u = ask("Enter domain: ")
    p = urlparse(u if "://" in u else "https://" + u)

    if p.scheme != "https" or not p.hostname:
        return fail("Invalid HTTPS address")

    ok("HTTPS URL format detected")
    print("This does not verify the live certificate.")


# 03 - Suspicious URL Checker
def suspicious_url():
    u = ask("Enter URL: ").lower()
    flags = []

    for word in [
        "login", "verify", "free", "prize",
        "account", "wallet", "password"
    ]:
        if word in u:
            flags.append(word)

    if "@" in u:
        flags.append("@ symbol")

    if "xn--" in u:
        flags.append("Punycode domain")

    if flags:
        warn("Review patterns: " + ", ".join(flags))
    else:
        ok("No listed patterns found")

    warn("Not a complete phishing detector.")


# 04 - Email Validator
def email_validator():
    e = ask("Email: ")

    if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", e):
        ok("Basic email format valid")
    else:
        fail("Invalid email format")


# 05 - Password Analyzer
def password_analyzer():
    p = ask("Enter TEST password: ")

    score = sum([
        len(p) >= 12,
        bool(re.search(r"[a-z]", p)),
        bool(re.search(r"[A-Z]", p)),
        bool(re.search(r"[0-9]", p)),
        bool(re.search(r"[^a-zA-Z0-9]", p))
    ])

    levels = [
        "Very weak", "Weak", "Fair",
        "Good", "Strong", "Strong"
    ]

    ok("Estimated strength: " + levels[score])
    warn("Basic estimate only. Never enter your real password.")


# 06 - Password Generator
def password_generator():
    chars = string.ascii_letters + string.digits + "!@#$%&*?"
    p = "".join(secrets.choice(chars) for _ in range(24))

    ok("Generated password: " + p)
    warn("Store securely. Do not share.")


# 07 - Text SHA256
def text_hash():
    t = ask("Enter text: ")
    ok(hashlib.sha256(t.encode()).hexdigest())


# 08 - File SHA256
def file_hash():
    p = Path(ask("File path: "))

    if not p.is_file():
        return fail("File not found")

    h = hashlib.sha256()

    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)

    ok("SHA256: " + h.hexdigest())


# 09 - File Metadata
def file_metadata():
    p = Path(ask("File path: "))

    if not p.is_file():
        return fail("File not found")

    s = p.stat()

    ok("Name: " + p.name)
    print("Size:", s.st_size, "bytes")
    print("Modified:", datetime.fromtimestamp(s.st_mtime))


# 10 - File Size
def file_size():
    p = Path(ask("File path: "))

    if p.is_file():
        ok(f"Size: {p.stat().st_size:,} bytes")
    else:
        fail("File not found")


# 11 - File Signature
def file_signature():
    p = Path(ask("File path: "))

    if not p.is_file():
        return fail("File not found")

    with p.open("rb") as f:
        header = f.read(16).hex()

    ok("File header: " + header)
    warn("Header inspection is not malware detection.")


# 12 - Directory Viewer
def directory_viewer():
    p = Path(ask("Folder path: "))

    if not p.is_dir():
        return fail("Folder not found")

    for item in list(p.iterdir())[:100]:
        print(
            C +
            ("DIR  " if item.is_dir() else "FILE ") +
            item.name +
            X
        )


# 13 - Duplicate Finder
def duplicate_finder():
    p = Path(ask("Folder path: "))

    if not p.is_dir():
        return fail("Folder not found")

    seen = {}

    for f in p.iterdir():
        if f.is_file():
            try:
                h = hashlib.sha256(f.read_bytes()).hexdigest()

                if h in seen:
                    warn(f"Duplicate: {f.name} = {seen[h]}")
                else:
                    seen[h] = f.name

            except OSError:
                warn("Cannot read: " + f.name)

    ok("Read-only scan complete")


# 14 - JSON Validator
def json_validator():
    try:
        data = json.loads(ask("Enter JSON: "))
        ok("Valid JSON: " + type(data).__name__)

    except json.JSONDecodeError as e:
        fail("Invalid JSON: " + str(e))


# 15 - Base64 Encoder
def base64_encoder():
    t = ask("Text: ")
    ok(base64.b64encode(t.encode()).decode())


# 16 - Base64 Decoder
def base64_decoder():
    t = ask("Base64: ")

    try:
        ok(base64.b64decode(t, validate=True).decode())
    except Exception:
        fail("Invalid Base64 or non-text data")


# 17 - DNS Lookup
def dns_lookup():
    host = ask("Domain: ")

    try:
        results = socket.getaddrinfo(host, None)
        ips = sorted(set(x[4][0] for x in results))

        for ip in ips:
            ok(ip)

    except socket.gaierror:
        fail("DNS lookup failed")


# 18 - IP Information
def ip_information():
    raw = ask("IP address: ")

    try:
        ip = ipaddress.ip_address(raw)

        ok("IP version: " + str(ip.version))
        print("Private:", ip.is_private)
        print("Global:", ip.is_global)
        print("Loopback:", ip.is_loopback)

    except ValueError:
        fail("Invalid IP")


# 19 - Internet Connectivity
def connectivity():
    try:
        s = socket.create_connection(
            ("example.com", 443),
            timeout=5
        )
        s.close()

        ok("Internet connection available")

    except OSError:
        fail("Connection unavailable")


# 20 - TLS Information
def tls_information():
    host = ask("Domain: ")

    try:
        ctx = ssl.create_default_context()

        with ctx.wrap_socket(
            socket.socket(),
            server_hostname=host
        ) as s:

            s.settimeout(5)
            s.connect((host, 443))

            cert = s.getpeercert()

            ok("TLS: " + str(s.version()))
            print("Certificate:", cert.get("subject"))
            print("Expires:", cert.get("notAfter"))

    except Exception as e:
        fail("TLS check failed: " + str(e))


# 21 - Local Network
def local_network():
    ok("Device: " + socket.gethostname())

    try:
        print(
            "Local IP:",
            socket.gethostbyname(socket.gethostname())
        )

    except OSError:
        warn("Local IP unavailable")


# 22 - Security Checklist
def security_checklist():
    tasks = [
        "Use unique passwords",
        "Enable 2FA",
        "Update software",
        "Backup important files",
        "Review login sessions",
        "Avoid unknown attachments"
    ]

    for item in tasks:
        print(G + "[ ] " + item + X)


# 23 - Random Token
def random_token():
    ok(secrets.token_urlsafe(32))


# 24 - UUID Generator
def uuid_generator():
    ok(str(uuid.uuid4()))


# 25 - Text Statistics
def text_statistics():
    t = ask("Enter text: ")

    print("Characters:", len(t))
    print("Words:", len(t.split()))
    print("Lines:", len(t.splitlines()))
    print("Digits:", sum(c.isdigit() for c in t))


# 26 - Extension Checker
def extension_checker():
    p = Path(ask("File name: "))
    ok("Extension: " + (p.suffix or "No extension"))


# 27 - Permission Checker
def permission_checker():
    p = Path(ask("File path: "))

    if not p.exists():
        return fail("Path not found")

    ok("Readable: " + str(os.access(p, os.R_OK)))
    print("Writable:", os.access(p, os.W_OK))
    print("Executable:", os.access(p, os.X_OK))


# 28 - System Information
def system_information():
    ok("OS: " + platform.system())
    print("Release:", platform.release())
    print("Python:", platform.python_version())
    print("Architecture:", platform.machine())


# 29 - Report Generator
def report_generator():
    data = (
        "CYBER LION SECURITY REPORT\n"
        "Generated: " + datetime.now().isoformat() + "\n"
        "Device: " + platform.system() + "\n"
        "Python: " + platform.python_version() + "\n"
        "Toolkit: V3.0\n"
        "Modules: 30\n"
    )

    Path("cyber_lion_report.txt").write_text(data)

    ok("Saved cyber_lion_report.txt")


# 30 - Toolkit Information
def toolkit_info():
    ok("CYBER LION SECURITY TOOLKIT V3.0")
    print("Created by: GOKU")
    print("Modules: 30")
    print("Platform: Termux / Linux")
    print("Purpose: Defensive security education")


modules = [
    ("URL Analyzer", url_analyzer),
    ("HTTPS Checker", https_checker),
    ("Suspicious URL Checker", suspicious_url),
    ("Email Validator", email_validator),
    ("Password Analyzer", password_analyzer),
    ("Password Generator", password_generator),
    ("Text SHA256 Generator", text_hash),
    ("File SHA256 Checker", file_hash),
    ("File Metadata Viewer", file_metadata),
    ("File Size Checker", file_size),
    ("File Signature Viewer", file_signature),
    ("Directory Viewer", directory_viewer),
    ("Duplicate File Finder", duplicate_finder),
    ("JSON Validator", json_validator),
    ("Base64 Encoder", base64_encoder),
    ("Base64 Decoder", base64_decoder),
    ("DNS Lookup", dns_lookup),
    ("IP Information", ip_information),
    ("Internet Connectivity", connectivity),
    ("TLS Certificate Viewer", tls_information),
    ("Local Network Information", local_network),
    ("Security Checklist", security_checklist),
    ("Random Token Generator", random_token),
    ("UUID Generator", uuid_generator),
    ("Text Statistics", text_statistics),
    ("File Extension Checker", extension_checker),
    ("File Permission Checker", permission_checker),
    ("System Information", system_information),
    ("Security Report Generator", report_generator),
    ("Toolkit Information", toolkit_info)
]


def main():
    while True:
        title()

        for i, (name, _) in enumerate(modules, 1):
            print(Y + f" [{i:02}] " + C + name + X)

        print(R + "\n [00] EXIT" + X)
        line()

        choice = ask("SELECT MODULE: ")

        if choice in ("0", "00"):
            ok("CYBER LION OFFLINE")
            break

        if choice.isdigit() and 1 <= int(choice) <= 30:
            try:
                modules[int(choice) - 1][1]()

            except KeyboardInterrupt:
                warn("Operation cancelled")

            except Exception as e:
                fail("Error: " + str(e))

            pause()

        else:
            fail("Select a number between 0 and 30")
            pause()


if __name__ == "__main__":
    main()
