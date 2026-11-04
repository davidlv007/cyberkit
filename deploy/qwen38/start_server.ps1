param(
    [string]$Root = "D:\AI\qwen38",
    [int]$Port = 8088,
    [int]$Context = 32768,
    [int]$ReasoningBudget = 512
)

$ErrorActionPreference = "Continue"
$runtime13 = Join-Path $Root "runtime\llama.cpp\b11146-cuda13.4"
$runtime12 = Join-Path $Root "runtime\llama.cpp\b11146-cuda12.4"
# 驱动 576.88 无法初始化 CUDA 13.4；12.4 构建可启动。驱动升级后再切 13.4。
$runtime = if (Test-Path (Join-Path $runtime12 "llama-server.exe")) { $runtime12 } elseif (Test-Path (Join-Path $runtime13 "llama-server.exe")) { $runtime13 } else { $runtime12 }
$modelPrimary = Join-Path $Root "models\Qwen3.8-27B-UD-Q6_K.gguf"
$modelFallback = Join-Path $Root "models\Qwen3.8-27B-UD-Q5_K_M.gguf"
$model = if (Test-Path $modelPrimary) { $modelPrimary } elseif (Test-Path $modelFallback) { $modelFallback } else { $null }

if (-not (Test-Path (Join-Path $runtime "llama-server.exe"))) {
    throw "llama-server.exe 不存在，请先完成 deploy 解压"
}
if (-not $model) {
    throw "GGUF 尚未下载完成: $modelPrimary"
}

$logDir = Join-Path $Root "logs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$log = Join-Path $logDir "llama-server.log"

Write-Host "runtime=$runtime"
Write-Host "model=$model"
Write-Host "listen=0.0.0.0:$Port (LAN)"

Set-Location $runtime
$argLine = "-m `"$model`" --no-mmproj -ngl 999 -c $Context -ctk q8_0 -ctv q8_0 --jinja --reasoning-budget $ReasoningBudget --host 0.0.0.0 --port $Port --parallel 1 --alias qwen3.8-27b"
cmd /c "llama-server.exe $argLine >> `"$log`" 2>&1"
