# 一键启动 cyberkit 全部依赖服务(开机后只需运行这一条)
#   powershell -ExecutionPolicy Bypass -File E:\cyberkit\deploy\start_all.ps1
#
# 顺序:llama.cpp(8088) -> GPT-SoVITS(9880,含注册+预热) -> 小智服务端(8000/8003)
# 已在监听的端口会自动跳过,不会重复启动;服务在后台窗口运行,日志在 deploy\logs\
$ErrorActionPreference = "Continue"

# IDE 注入的 Python 删除拦截 shim 会干扰模型脚本,启动前清掉
Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue

$deploy = "E:\cyberkit\deploy"
$logDir = Join-Path $deploy "logs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

function Test-Port {
    param([int]$Port)
    return [bool](Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue)
}

function Wait-Port {
    param([int]$Port, [int]$TimeoutSec, [string]$Name, [string]$HintLog)
    $elapsed = 0
    while ($elapsed -lt $TimeoutSec) {
        if (Test-Port $Port) {
            Write-Host ("  [OK] " + $Name + " 端口 " + $Port + " 就绪(" + $elapsed + "s)")
            return $true
        }
        Start-Sleep -Seconds 3
        $elapsed += 3
    }
    Write-Host ("  [超时] " + $Name + " 端口 " + $Port + " 未就绪,请查日志: " + $HintLog)
    return $false
}

function Start-BackgroundService {
    param([string]$Script, [string]$OutLog, [string]$ErrLog)
    Start-Process powershell -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File',$Script -WindowStyle Hidden -RedirectStandardOutput (Join-Path $logDir $OutLog) -RedirectStandardError (Join-Path $logDir $ErrLog) | Out-Null
}

Write-Host "==================== cyberkit 一键启动 ===================="

# ---------- 1. llama.cpp 模型服务 ----------
Write-Host "[1/3] llama.cpp 模型服务 (8088)"
if (Test-Port 8088) {
    Write-Host "  已在运行,跳过"
} else {
    Start-BackgroundService (Join-Path $deploy "qwen38\start_server.ps1") "llama_start.log" "llama_start_err.log"
    Write-Host "  启动中(GGUF 加载约 1 分钟)..."
    [void](Wait-Port 8088 300 "llama.cpp" "D:\AI\qwen38\logs\llama-server.log")
}

# ---------- 2. GPT-SoVITS TTS ----------
Write-Host "[2/3] GPT-SoVITS v2Pro (9880)"
if (Test-Port 9880) {
    Write-Host "  已在运行,跳过(若刚重启过且未注册 speaker,请单独跑一次 GPT-SoVITS\start_api.ps1)"
} else {
    # 该脚本自包含:启动 api.py -> 等端口 -> /set_model 注册 -> 预热
    # 用独立进程 -Wait 隔离(它内部失败时会 exit 1)
    $gsvScript = Join-Path $deploy "GPT-SoVITS\start_api.ps1"
    Start-Process powershell -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File',$gsvScript -Wait -WindowStyle Hidden -RedirectStandardOutput (Join-Path $logDir "gsv_start.log") -RedirectStandardError (Join-Path $logDir "gsv_start_err.log") | Out-Null
    Get-Content (Join-Path $logDir "gsv_start.log") -ErrorAction SilentlyContinue | Select-Object -Last 6 | ForEach-Object { Write-Host ("  " + $_) }
}

# ---------- 3. 小智服务端 ----------
Write-Host "[3/3] 小智服务端 (8000 / 8003)"
if ((Test-Port 8000) -and (Test-Port 8003)) {
    Write-Host "  已在运行,跳过"
} else {
    Start-BackgroundService (Join-Path $deploy "xiaozhi-esp32-server\start_server.ps1") "xiaozhi_start.log" "xiaozhi_start_err.log"
    Write-Host "  启动中(ASR 模型加载约 40 秒)..."
    [void](Wait-Port 8000 180 "小智 WebSocket" (Join-Path $logDir "xiaozhi_start_err.log"))
    [void](Wait-Port 8003 60 "小智 OTA" (Join-Path $logDir "xiaozhi_start_err.log"))
}

# ---------- 汇总 ----------
Write-Host ""
Write-Host "==================== 服务状态 ===================="
foreach ($p in @(8088, 9880, 8000, 8003)) {
    $state = if (Test-Port $p) { "UP  " } else { "DOWN" }
    $name = switch ($p) {
        8088 { "llama.cpp 模型服务" }
        9880 { "GPT-SoVITS TTS   " }
        8000 { "小智 WebSocket    " }
        8003 { "小智 OTA / HTTP   " }
    }
    Write-Host ("  [" + $state + "] " + $p + "  " + $name)
}
Write-Host ""
Write-Host "全部就绪后给喵伴设备上电即可(设备连 WiFi 后会自动连本机)。"
Write-Host ("启动日志目录: " + $logDir)
Write-Host "=========================================================="
