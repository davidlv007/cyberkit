Write-Host "=== COM 端口列表 ==="
Get-CimInstance Win32_SerialPort -ErrorAction SilentlyContinue |
    Select-Object DeviceID, Description | Format-Table -AutoSize

Write-Host "=== COM8 是否被占用 ==="
$h = Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -like "*COM8*" }
if ($h) {
    $h | Select-Object ProcessId, Name, CreationDate, CommandLine | Format-List
} else {
    Write-Host "  无进程占用 COM8"
}

Write-Host "=== esptool / python 烧录进程 ==="
$p = Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -like "*esptool*" -or $_.CommandLine -like "*write_flash*" }
if ($p) {
    $p | Select-Object ProcessId, Name, CreationDate | Format-Table -AutoSize
} else {
    Write-Host "  无"
}

Write-Host "=== 固件包 ==="
Get-Item "E:\cyberkit\releases\v2.0.5.6_CyberVoc-Board-V2_1.zip" |
    Select-Object Name, Length, LastWriteTime | Format-List
