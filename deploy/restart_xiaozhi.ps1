# 重启小智服务端(按端口精确杀,避免误杀其他 python)
$ErrorActionPreference = "SilentlyContinue"
$c = Get-NetTCPConnection -State Listen -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -First 1
if ($c) {
    Write-Host ("停止旧实例 PID " + $c.OwningProcess)
    Stop-Process -Id $c.OwningProcess -Force
}
Start-Sleep -Seconds 3
& "E:\cyberkit\deploy\start_all.ps1"
