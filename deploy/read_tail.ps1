$f = "e:\cyberkit\deploy\xiaozhi-esp32-server\main\xiaozhi-server\tmp\server.log"
Write-Host "=== 日志尾部 25 行(截断长行) ==="
Get-Content $f -Tail 25 | ForEach-Object {
    if ($_.Length -gt 260) { Write-Host ($_.Substring(0, 260) + "...") } else { Write-Host $_ }
}
