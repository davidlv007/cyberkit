# 停掉旧 llama-server 并用新参数重启
$ErrorActionPreference = "Continue"
Get-Process llama-server -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 3
# 启动新的(llama 模型加载需要 30-60 秒)
Start-Process powershell -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','e:\cyberkit\deploy\qwen38\start_server.ps1' -WindowStyle Hidden
Write-Host "new llama-server starting..."
