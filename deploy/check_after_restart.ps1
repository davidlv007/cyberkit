$f = "e:\cyberkit\deploy\xiaozhi-esp32-server\main\xiaozhi-server\tmp\server.log"
Write-Host "=== 最近一次服务启动 ==="
Select-String -Path $f -Pattern "启动全局GC管理器" | Select-Object -Last 1 | ForEach-Object { Write-Host $_.Line }
Write-Host ""
Write-Host "=== 噪声过滤日志(应只有重启后才有) ==="
Select-String -Path $f -Pattern "忽略噪声识别结果" | Select-Object -Last 12 | ForEach-Object { Write-Host $_.Line }
Write-Host ""
Write-Host "=== 日志最后 12 行 ==="
Get-Content $f -Tail 12 | ForEach-Object { if ($_.Length -gt 240) { Write-Host ($_.Substring(0,240) + "...") } else { Write-Host $_ } }
