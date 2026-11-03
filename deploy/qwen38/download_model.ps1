param(
    [string]$Root = "D:\AI\qwen38",
    [string]$Mirror = "https://hf-mirror.com"
)

$ErrorActionPreference = "Stop"
$destDir = Join-Path $Root "models"
New-Item -ItemType Directory -Force -Path $destDir | Out-Null
$url = "$Mirror/unsloth/Qwen3.8-27B-GGUF/resolve/main/Qwen3.8-27B-UD-Q6_K.gguf"
$out = Join-Path $destDir "Qwen3.8-27B-UD-Q6_K.gguf"
Write-Host "GET $url"
Write-Host "OUT $out"
curl.exe -L --retry 12 --retry-delay 5 -C - -o $out $url
Get-Item $out | Select-Object FullName, Length
