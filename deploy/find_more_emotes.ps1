Write-Host "=== 三个板级 eaf 内容是否相同(MD5) ==="
foreach ($b in @("CyberVoc-Board-V1_2", "CyberVoc-Board-V2_0", "CyberVoc-Board-V2_1")) {
    $p = "e:\cyberkit\main\boards\$b\assets\emoji_large"
    $h = (Get-ChildItem $p -Filter "*.eaf" | Sort-Object Name | Get-FileHash -Algorithm MD5 | ForEach-Object { $_.Hash }) -join ""
    $combined = [System.Text.Encoding]::UTF8.GetBytes($h)
    $md5 = [System.Security.Cryptography.MD5]::Create()
    $sum = [BitConverter]::ToString($md5.ComputeHash($combined)).Replace("-", "")
    Write-Host ("  " + $b + " -> " + $sum.Substring(0, 12))
}

Write-Host ""
Write-Host "=== 组件自带成品 assets.bin ==="
Get-ChildItem "e:\cyberkit\managed_components\espressif2022__esp_emote_assets" -Recurse -Include "*.bin","*.eaf" -ErrorAction SilentlyContinue |
    Select-Object FullName, Length | Format-Table -AutoSize

Write-Host "=== 仓库内所有 eaf(排除板级三套) ==="
Get-ChildItem "e:\cyberkit" -Recurse -Filter "*.eaf" -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notlike "*CyberVoc-Board-V*_2*" -and $_.FullName -notlike "*\build*\" } |
    Select-Object -First 30 FullName, Length | Format-Table -AutoSize
