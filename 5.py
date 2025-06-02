x = """$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -Command `"Write-Output 'Bu bir testtir'`""
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) # 1 dakika sonra çalışacak
Register-ScheduledTask -TaskName "TestMaliciousTask" -Action $Action -Trigger $Trigger -User "SYSTEM" -RunLevel Highest"""
print("----------------EXPLOIT------------------")
print(x)
