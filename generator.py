import os

def run_pyload(choice):
    if choice == "p1":
        os.system("python3 p1.py")
    elif choice == "p2":
        os.system("python3 p2.py")
    elif choice == "p3":
        os.system("python3 p3.py")
    elif choice == "p4":
        os.system("python3 p4.py")

def run_c2(choice):
    if choice == "c1":
        os.system("python3 c.py")
    elif choice == "c2":
        os.system("python3 c1.py")

def run_antibypass(choice):
    if choice == "b":
        os.system("python3 b.py")
    elif choice == "b2":
        os.system("python3 b2.py")
    elif choice == "b3":
        os.system("python3 b3.py")
    elif choice == "b4":
        os.system("python3 b4.py")
    elif choice == "b5":
        os.system("python3 b5.py")

def run_exploit(choice):
    if choice == "x":
        os.system("python3 1.py")
    elif choice == "x2":
        os.system("python3 2.py")
    elif choice == "x3":
        os.system("python3 3.py")
    elif choice == "x4":
        os.system("python3 4.py")
    elif choice == "x5":
        os.system("python3 5.py")

if __name__ == "__main__":
    x = input("Pyloadinizi seçin: ")
    y = input("C2 kanalınızı seçin: ")
    z = input("Anti bypassınızı seçin: ")
    c = input("Exploitinizi seçin: ")

    run_pyload(x)
    run_c2(y)
    run_antibypass(z)
    run_exploit(c)

    print("Başarıyla oluşturuldu!")
