# PowerShell script to start Django server with explicit port
Write-Host "Activating virtual environment..." -ForegroundColor Green
& "$PSScriptRoot\venv\Scripts\Activate.ps1"

Write-Host "`nStarting Django development server..." -ForegroundColor Green
Write-Host "Open your browser and navigate to: http://127.0.0.1:9090/" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server`n" -ForegroundColor Yellow

# Run Django server on port 9090, bind to all interfaces
$process = Start-Process -FilePath python -ArgumentList "manage.py", "runserver", "0.0.0.0:9090" -NoNewWindow -PassThru

# Wait for user to press a key
Write-Host "Server is running. Press any key to stop the server..." -ForegroundColor Green
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Stop the server
Write-Host "`nStopping server..." -ForegroundColor Yellow
Stop-Process -Id $process.Id -Force
Write-Host "Server stopped." -ForegroundColor Green

# Keep the window open
Write-Host "`nPress any key to close this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 