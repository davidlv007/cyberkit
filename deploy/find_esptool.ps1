$candidates = @(
    "E:\cyberkit\deploy\GPT-SoVITS\.venv\Scripts\python.exe",
    "E:\cyberkit\deploy\xiaozhi-esp32-server\.venv\Scripts\python.exe",
    "C:\Espressif\tools\python\python.exe",
    "C:\idf5.5.2\python_env\Scripts\python.exe",
    "C:\esp\v5.5.2\esp-idf\python_env\Scripts\python.exe"
)
foreach ($p in $candidates) {
    if (Test-Path $p) {
        $out = & $p -c "import esptool; print(esptool.__version__)" 2>&1
        Write-Host ("{0} -> {1}" -f $p, ($out | Select-Object -Last 1))
    }
}
Write-Host ""
Write-Host "=== 查找 esptool.exe / esptool.py ==="
Get-ChildItem "C:\Espressif", "C:\idf5.5.2", "C:\esp" -Recurse -Filter "esptool*" -ErrorAction SilentlyContinue |
    Select-Object -First 12 FullName | Format-Table -AutoSize
