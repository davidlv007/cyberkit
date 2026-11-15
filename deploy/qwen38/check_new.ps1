Write-Host "=== llama-server 进程命令行 ==="
Get-CimInstance Win32_Process -Filter "Name='llama-server.exe'" |
    Select-Object ProcessId, CreationDate, CommandLine | Format-List

Write-Host "=== 端口 8088 ==="
Get-NetTCPConnection -State Listen -LocalPort 8088 -ErrorAction SilentlyContinue |
    Select-Object LocalAddress, LocalPort, OwningProcess | Format-Table -AutoSize

Write-Host "=== 日志里最近的启动/监听标志 ==="
$log = "D:\AI\qwen38\logs\llama-server.log"
if (Test-Path $log) {
    Select-String -Path $log -Pattern "flash_attn|server is listening|main: server|reasoning" |
        Select-Object -Last 8 | ForEach-Object { $_.Line }
}
