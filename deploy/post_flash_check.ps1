$log = "e:\cyberkit\deploy\flash.log"
Write-Host "=== 烧录结果关键行 ==="
Select-String -Path $log -Pattern "Wrote |Hash of data verified|Leaving|Hard resetting|ESPTOOL_EXIT" |
    ForEach-Object { Write-Host ("  " + $_.Line.Trim()) }

Write-Host ""
Write-Host "=== 残留 esptool 进程数 ==="
$n = (Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
      Where-Object { $_.CommandLine -like "*esptool*" } | Measure-Object).Count
Write-Host ("  " + $n)

Write-Host ""
Write-Host "=== 设备重启后是否连回小智服务端 ==="
$srv = "e:\cyberkit\deploy\xiaozhi-esp32-server\main\xiaozhi-server\tmp\server.log"
Select-String -Path $srv -Pattern "收到hello消息|收到listen消息|Headers:" |
    Select-Object -Last 6 | ForEach-Object { Write-Host ("  " + $_.Line.Trim()) }

Write-Host ""
Write-Host "=== 服务端口 ==="
foreach ($p in @(8088, 9880, 8000, 8003)) {
    $c = Get-NetTCPConnection -State Listen -LocalPort $p -ErrorAction SilentlyContinue
    Write-Host ("  " + $p + ": " + $(if ($c) { "UP" } else { "DOWN" }))
}
