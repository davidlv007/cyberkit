Write-Host "=== 组件自带表情包(360_360) ==="
Get-ChildItem "e:\cyberkit\managed_components\espressif2022__esp_emote_assets\360_360" -Recurse -File -ErrorAction SilentlyContinue |
    Select-Object Name, Length | Format-Table -AutoSize

Write-Host "=== 各板级 eaf 数量 ==="
foreach ($b in @("CyberVoc-Board-V1_2", "CyberVoc-Board-V2_0", "CyberVoc-Board-V2_1")) {
    $p = "e:\cyberkit\main\boards\$b\assets\emoji_large"
    $n = (Get-ChildItem $p -Filter "*.eaf" -ErrorAction SilentlyContinue | Measure-Object).Count
    Write-Host ("  " + $b + ": " + $n + " 个 .eaf")
}

Write-Host "=== 360_360 目录下的配置/布局文件 ==="
Get-ChildItem "e:\cyberkit\main\boards\CyberVoc-Board-V2_1\assets\360_360" -ErrorAction SilentlyContinue |
    Select-Object Name, Length | Format-Table -AutoSize
