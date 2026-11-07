$zip = "E:\cyberkit\deploy\emote_preview\EmotePack.zip"
$dst = "E:\cyberkit\deploy\emote_preview\EmotePack"
if (Test-Path $dst) { Remove-Item $dst -Recurse -Force }
Expand-Archive -Path $zip -DestinationPath $dst -Force

Write-Host "=== 目录结构 ==="
Get-ChildItem $dst -Directory | Select-Object Name | Format-Table -AutoSize
Write-Host ""
Write-Host "=== 文件类型统计 ==="
Get-ChildItem $dst -Recurse -File | Group-Object Extension | Sort-Object Count -Descending |
    Select-Object Name, Count | Format-Table -AutoSize
Write-Host ""
Write-Host "=== 顶层文件/目录(前 40) ==="
Get-ChildItem $dst -Recurse -File | Select-Object -First 40 FullName, Length | Format-Table -AutoSize
