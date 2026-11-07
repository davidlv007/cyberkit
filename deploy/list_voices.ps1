$py = "E:\cyberkit\deploy\xiaozhi-esp32-server\.venv\Scripts\python.exe"
$out = & $py -m edge_tts --list-voices 2>&1 | Out-String
$out -split "`n" | Where-Object { $_ -match "zh-CN.*(Female|Xiaoshuang|Xiaoyi|Xiaoxiao)" } | ForEach-Object { Write-Host $_.Trim() }
