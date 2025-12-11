<# Run tests (Windows PowerShell) using the local venv python
   Usage: .\scripts\run_tests.ps1
#>
$python = Join-Path -Path $PSScriptRoot -ChildPath "..\.venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    $python = "python"
}

# Run tests with a flag to disable interactive popups (useful in CI and automated runs)
$env:REBUILD_DISABLE_AUTO_POPUPS = '1'
Start-Process -FilePath $python -ArgumentList "-m pytest -q" -NoNewWindow -Wait -WorkingDirectory "$(Resolve-Path $PSScriptRoot\.. )"
