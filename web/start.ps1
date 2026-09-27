$ErrorActionPreference = 'Stop'
$siteRoot = $PSScriptRoot
$siteUrl = 'http://127.0.0.1:3760'
$siteReady = $false
try {
    $health = Invoke-RestMethod "$siteUrl/api/health" -TimeoutSec 2
    $siteReady = $health.app -eq 'course-study-desk'
} catch { }
if (-not $siteReady) {
    $nodePath = (Get-Command node -ErrorAction Stop).Source
    if (-not (Test-Path -LiteralPath (Join-Path $siteRoot 'node_modules\katex\dist\katex.min.js'))) {
        throw 'Math assets are missing. Run npm install in this folder once, then retry.'
    }
    Start-Process -FilePath $nodePath -ArgumentList ('"' + (Join-Path $siteRoot 'server.mjs') + '"') -WorkingDirectory $siteRoot -WindowStyle Hidden -RedirectStandardOutput (Join-Path $siteRoot 'server.log') -RedirectStandardError (Join-Path $siteRoot 'server-error.log')
    for ($attempt = 0; $attempt -lt 20; $attempt++) {
        Start-Sleep -Milliseconds 250
        try { $health = Invoke-RestMethod "$siteUrl/api/health" -TimeoutSec 1; if ($health.app -eq 'course-study-desk') { $siteReady=$true; break } } catch { }
    }
}
if (-not $siteReady) { throw 'Could not start the website. Port 3760 may be occupied; check server-error.log.' }
Start-Process $siteUrl
