<# Run the app (Windows PowerShell)
   This runs the local virtualenv python to execute the app launcher.
   Usage: .\scripts\run_app.ps1
#>
$python = Join-Path -Path $PSScriptRoot -ChildPath "..\.venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    $python = "python"
}

Start-Process -FilePath $python -ArgumentList "-m src.platform.launcher" -NoNewWindow -Wait
