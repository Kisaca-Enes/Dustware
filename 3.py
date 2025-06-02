x = """

import wmi

def wmi_powershell_execute(payload):
    c = wmi.WMI()
    # PowerShell komutunu gizli pencerede çalıştır
    command = f'powershell.exe -windowstyle hidden -command "{payload}"'
    process_id, result = c.Win32_Process.Create(CommandLine=command)
    if result == 0:
        print(f"[+] Process created with PID {process_id}")
    else:
        print(f"[-] Failed to create process, error code: {result}")

if __name__ == "__main__":
    # Buraya gerçek PowerShell payload’unu yazabilirsin
    powershell_payload = 'Write-Output "Merhaba, WMI üzerinden çalıştı!" > C:\\temp\\output.txt'
    wmi_powershell_execute(powershell_payload)



"""
print(x)