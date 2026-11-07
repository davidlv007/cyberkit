Write-Host "=== USB 串口 / CH340 / ESP 相关 PnP 设备 ==="
Get-PnpDevice -ErrorAction SilentlyContinue |
    Where-Object { $_.FriendlyName -match "CH340|USB-SERIAL|USB Serial|CP210|FTDI|ESP|JTAG|USB.*Serial" -or
                   $_.InstanceId -match "VID_1A86|VID_303A|VID_10C4" } |
    Select-Object Status, Class, FriendlyName, InstanceId | Format-List

Write-Host "=== 有问题的 USB/端口设备(Error/Unknown) ==="
Get-PnpDevice -Class Ports, USB -ErrorAction SilentlyContinue |
    Where-Object { $_.Status -ne "OK" } |
    Select-Object Status, Class, FriendlyName, InstanceId | Format-Table -AutoSize
