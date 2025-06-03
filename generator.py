import subprocess

def run_script(script_path, label):
    try:
        print(f"[+] {label} çalıştırılıyor: {script_path}")
        subprocess.run(["python3", script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] Hata ({label}): {e}")
    except FileNotFoundError:
        print(f"[!] Dosya bulunamadı ({label}): {script_path}")

def run_pyload(choice):
    scripts = {
        "p1": "p1.py",
        "p2": "p2.py",
        "p3": "p3.py",
        "p4": "p4.py"
    }
    if choice in scripts:
        run_script(scripts[choice], "Pyload")
    else:
        print("[!] Geçersiz pyload seçimi.")

def run_c2(choice):
    scripts = {
        "c1": "c.py",
        "c2": "c1.py"
    }
    if choice in scripts:
        run_script(scripts[choice], "C2")
    else:
        print("[!] Geçersiz C2 seçimi.")

def run_antibypass(choice):
    scripts = {
        "b": "b.py",
        "b2": "b2.py",
        "b3": "b3.py",
        "b4": "b4.py",
        "b5": "b5.py"
    }
    if choice in scripts:
        run_script(scripts[choice], "Anti-Bypass")
    else:
        print("[!] Geçersiz Anti-Bypass seçimi.")

def run_exploit(choice):
    scripts = {
        "x": "1.py",
        "x2": "2.py",
        "x3": "3.py",
        "x4": "4.py",
        "x5": "5.py"
    }
    if choice in scripts:
        run_script(scripts[choice], "Exploit")
    else:
        print("[!] Geçersiz exploit seçimi.")

if __name__ == "__main__":
    print("==== Seçim Ekranı ====")
    x = input("Pyload'inizi seçin (p1, p2, p3, p4): ")
    y = input("C2 kanalınızı seçin (c1, c2): ")
    z = input("Anti bypass seçin (b, b2, b3, b4, b5): ")
    c = input("Exploit seçin (x, x2, x3, x4, x5): ")

    print("\n==== Çalıştırılıyor ====")
    run_pyload(x)
    run_c2(y)
    run_antibypass(z)
    run_exploit(c)

    print("\n[+] Tüm işlemler tamamlandı.")
