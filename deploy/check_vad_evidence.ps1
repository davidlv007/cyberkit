# 最近日志短行全文(排除 mcp 大 JSON),看 VAD 报错/ASR 结果/超时细节
$f = "E:\cyberkit\deploy\xiaozhi-esp32-server\main\xiaozhi-server\tmp\server.log"
$lines = Get-Content $f -Tail 250
foreach ($l in $lines) {
    if ($l.Length -gt 400) { continue }
    Write-Host $l
}
