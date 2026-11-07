# 找最新的服务端日志并提取 ASR/VAD/listen 相关行
$ErrorActionPreference = "SilentlyContinue"
$root = "E:\cyberkit\deploy\xiaozhi-esp32-server\main\xiaozhi-server"
$candidates = @(
    "$root\tmp\server.log",
    "E:\cyberkit\deploy\logs\xiaozhi_start.log",
    "E:\cyberkit\deploy\logs\xiaozhi_start_err.log",
    "E:\cyberkit\deploy\xiaozhi-esp32-server\server_out.log"
)
foreach ($f in $candidates) {
    if (Test-Path $f) {
        $item = Get-Item $f
        Write-Host ("=== " + $f + "  (" + $item.Length + " bytes, " + $item.LastWriteTime + ") ===")
        Get-Content $f -Tail 60 | Select-String -Pattern "listen|VAD|vad|ASR|asr|识别|静音|stop|start|ERROR|WARN" |
            Select-Object -Last 25 | ForEach-Object { Write-Host ("  " + $_.Line) }
    }
}
