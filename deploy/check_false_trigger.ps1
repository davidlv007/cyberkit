$f = "e:\cyberkit\deploy\xiaozhi-esp32-server\main\xiaozhi-server\tmp\server.log"
Write-Host "=== 最近 AUDIO_DIAG 25 条 ==="
Select-String -Path $f -Pattern "AUDIO_DIAG" | Select-Object -Last 25 | ForEach-Object { Write-Host $_.Line }
Write-Host ""
Write-Host "=== 最近识别文本 / 大模型收到 / 空识别 25 条 ==="
Select-String -Path $f -Pattern "识别文本|大模型收到用户消息|识别文本：空|ASR识别失败|语音生成失败" |
    Select-Object -Last 25 | ForEach-Object { Write-Host $_.Line }
