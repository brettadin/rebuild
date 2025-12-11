<# Run tests (Windows PowerShell) using the local venv python
   Usage: .\scripts\run_tests.ps1
#>
$python = Join-Path -Path $PSScriptRoot -ChildPath "..\.venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    $python = "python"
}

Start-Process -FilePath $python -ArgumentList "-m pytest -q" -NoNewWindow -Wait
