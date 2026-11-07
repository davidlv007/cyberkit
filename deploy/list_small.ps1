$p = "e:\cyberkit\managed_components\espressif2022__esp_emote_assets\emoji_small"
Write-Host "=== emoji_small 文件 ==="
Get-ChildItem $p -Filter "*.eaf" | Select-Object Name, Length | Format-Table -AutoSize
Write-Host "=== 组件 360_360 emote.json ==="
Get-Content "e:\cyberkit\managed_components\espressif2022__esp_emote_assets\360_360\emote.json" -Raw
