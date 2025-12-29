$ErrorActionPreference = "Stop"

# Define path
$SolutionPath = "$PSScriptRoot/../src/NvidiaControlPanel/NvidiaControlPanel.sln"

Write-Host "Running dotnet format on $SolutionPath..." -ForegroundColor Cyan
dotnet format $SolutionPath

Write-Host "Formatting Complete." -ForegroundColor Green
exit 0
