$ErrorActionPreference = "Continue"
Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
Set-Location E:\cyberkit\releases

$esptool = "C:\Espressif\tools\python\v5.5.2\venv\Scripts\esptool.exe"
Write-Host "开始烧录 COM8 (esptool 4.13.0 / IDF v5.5.2) ..."
& $esptool --chip esp32s3 -p COM8 -b 460800 `
    --before default_reset --after hard_reset `
    write_flash --flash_mode dio --flash_size 16MB --flash_freq 80m `
    0x0 merged-binary.bin
Write-Host "ESPTOOL_EXIT=$LASTEXITCODE"
