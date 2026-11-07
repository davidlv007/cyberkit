$ErrorActionPreference = "Continue"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$url = "https://dl.espressif.com/AE/Emote%20Pack.zip"
$out = "E:\cyberkit\deploy\emote_preview\EmotePack.zip"

try {
    $req = [Net.HttpWebRequest]::Create($url)
    $req.Method = "HEAD"
    $req.Timeout = 20000
    $resp = $req.GetResponse()
    Write-Host ("大小: " + [math]::Round($resp.ContentLength / 1MB, 2) + " MB, 类型: " + $resp.ContentType)
    $resp.Close()
} catch {
    Write-Host ("HEAD 失败: " + $_.Exception.Message)
}

try {
    Write-Host "下载中..."
    Invoke-WebRequest -Uri $url -OutFile $out -TimeoutSec 180
    $f = Get-Item $out
    Write-Host ("完成: " + [math]::Round($f.Length / 1MB, 2) + " MB")
} catch {
    Write-Host ("下载失败: " + $_.Exception.Message)
}
