$f = "e:\cyberkit\deploy\xiaozhi-esp32-server\main\xiaozhi-server\tmp\server.log"
Select-String -Path $f -Pattern "AUDIO_DIAG|收到listen消息" |
    Select-Object -Last 20 | ForEach-Object { Write-Host $_.Line }
