#!/usr/bin/env python3
"""
php2shell - reverse shell listener (authorised lab use only).
Listens on HOST:PORT, gives an interactive prompt. Standard library only.
Usage: python3 listener.py [HOST] [PORT]   (default 0.0.0.0 4444)
"""
import socket, sys, threading

def recv_loop(conn):
    while True:
        try:
            data = conn.recv(4096)
            if not data:
                print("\n[!] Connection closed by remote."); break
            sys.stdout.write(data.decode(errors="replace")); sys.stdout.flush()
        except OSError:
            break

def main():
    host = sys.argv[1] if len(sys.argv) > 1 else "0.0.0.0"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 4444
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((host, port)); srv.listen(1)
    print(f"[*] Listening on {host}:{port} ...")
    conn, addr = srv.accept()
    print(f"[+] Shell from {addr[0]}:{addr[1]}")
    threading.Thread(target=recv_loop, args=(conn,), daemon=True).start()
    try:
        for line in sys.stdin:
            conn.sendall(line.encode())
    except (BrokenPipeError, OSError):
        pass
    finally:
        conn.close(); srv.close(); print("[*] Listener stopped.")

if __name__ == "__main__":
    main()
