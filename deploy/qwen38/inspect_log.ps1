$lines = Get-Content "D:\AI\qwen38\logs\llama-server.log"
$idx = 0
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match "build:") { $idx = $i }
}
Write-Host "=== 最后一次启动块(build: 附近,第 $idx 行起 45 行) ==="
$start = [Math]::Max(0, $idx - 2)
$end = [Math]::Min($lines.Count - 1, $idx + 45)
for ($i = $start; $i -le $end; $i++) { Write-Host $lines[$i] }
