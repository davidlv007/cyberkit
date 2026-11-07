# 提取最近 listen/ASR/VAD/stop 相关日志(排除超长 mcp JSON 行)
$f = "E:\cyberkit\deploy\xiaozhi-esp32-server\main\xiaozhi-server\tmp\server.log"
$lines = Get-Content $f -Tail 400
foreach ($l in $lines) {
    if ($l.Length -gt 500) { continue }
    if ($l -match "listen|识别|ASR|asr|VAD|vad|stop|start|语音|唤醒|超时|timeout|ERROR|WARN") {
        Write-Host $l
    }
}
