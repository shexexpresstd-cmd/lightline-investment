# Start Flask and create tunnel
$ErrorActionPreference = "SilentlyContinue"

Write-Host "Starting Flask server..." -ForegroundColor Cyan
$flaskJob = Start-Job -ScriptBlock {
    Set-Location "C:\Users\MOHAMED\.qwenpaw\workspaces\default\lightline-investment"
    & python app.py
}

Start-Sleep -Seconds 5

Write-Host "Creating public tunnel..." -ForegroundColor Cyan
$ltJob = Start-Job -ScriptBlock {
    npx localtunnel --port 5000
}

Write-Host "Waiting for tunnel URL..." -ForegroundColor Yellow

for ($i = 0; $i -lt 15; $i++) {
    Start-Sleep -Seconds 1
    $output = Receive-Job $ltJob
    foreach ($line in $output) {
        if ($line -match "https?://") {
            Write-Host ""
            Write-Host "============================================" -ForegroundColor Green
            Write-Host "YOUR PUBLIC URL IS READY!" -ForegroundColor Green
            Write-Host "============================================" -ForegroundColor Green
            Write-Host $line -ForegroundColor Yellow
            Write-Host "============================================" -ForegroundColor Green
            Write-Host ""
            Write-Host "Server: http://127.0.0.1:5000" -ForegroundColor Cyan
            Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray
            break
        }
    }
}

Write-Host "Keeping server running... Press any key to stop" -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
Stop-Job -Job $flaskJob, $ltJob
Remove-Job -Job $flaskJob, $ltJob
