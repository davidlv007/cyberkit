$f = "e:\cyberkit\deploy\xiaozhi-esp32-server\main\xiaozhi-server\tmp\server.log"
Select-String -Path $f -Pattern "SileroVAD" | Select-Object -Last 3 | ForEach-Object { Write-Host $_.Line }
Write-Host ""
Write-Host "=== 最近 AUDIO_DIAG(重启后) ==="
Select-String -Path $f -Pattern "AUDIO_DIAG" | Select-Object -Last 5 | ForEach-Object { Write-Host $_.Line }
