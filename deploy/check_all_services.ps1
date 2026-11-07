# 检查项目全部依赖服务状态
$ErrorActionPreference = "SilentlyContinue"
$ports = @(8088, 8000, 8003, 9880)
foreach ($p in $ports) {
    $c = Get-NetTCPConnection -State Listen -LocalPort $p -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($c) {
        $proc = Get-CimInstance Win32_Process -Filter ("ProcessId=" + $c.OwningProcess)
        $name = $proc.Name
        Write-Host ("[UP]   " + $p + "  " + $c.LocalAddress + "  PID=" + $c.OwningProcess + "  " + $name)
    } else {
        Write-Host ("[DOWN] " + $p)
    }
}
Write-Host ""
Write-Host "=== 关键进程 ==="
Get-Process llama-server, python -ErrorAction SilentlyContinue |
    Select-Object Id, ProcessName, StartTime | Sort-Object ProcessName | Format-Table -AutoSize
Write-Host "=== IBXDashboard(已禁用,确认不占 8000) ==="
Get-Service IBXDashboard -ErrorAction SilentlyContinue | Select-Object Name, Status, StartType | Format-List
