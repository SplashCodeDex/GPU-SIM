$ErrorActionPreference = "Stop"

Write-Host "Starting Verification Routine..." -ForegroundColor Cyan

# Define paths
$SolutionPath = "$PSScriptRoot/../src/NvidiaControlPanel/NvidiaControlPanel.csproj"
$TestPath = "$PSScriptRoot/../src/NvidiaControlPanel.Tests/NvidiaControlPanel.Tests.csproj"

# 1. Clean
Write-Host "1. Cleaning..." -ForegroundColor Yellow
dotnet clean $SolutionPath
if ($LASTEXITCODE -ne 0) { Write-Error "Clean failed!"; exit 1 }

# 2. Format Check (Linting)
Write-Host "2. Checking Formatting..." -ForegroundColor Yellow
dotnet format $SolutionPath --verify-no-changes
if ($LASTEXITCODE -ne 0) { Write-Error "Formatting violations found! Run 'scripts/format.ps1' to fix."; exit 1 }

# 3. Build (Strict Mode is enabled in csproj)
Write-Host "3. Building (Strict Mode)..." -ForegroundColor Yellow
dotnet build $SolutionPath --configuration Release
if ($LASTEXITCODE -ne 0) { Write-Error "Build failed! Fix lint errors."; exit 1 }

# 3. Test
Write-Host "3. Running Tests..." -ForegroundColor Yellow
dotnet test $TestPath
if ($LASTEXITCODE -ne 0) { Write-Error "Tests failed!"; exit 1 }

Write-Host "VERIFICATION SUCCESSFUL. Workspace is clean and valid." -ForegroundColor Green
exit 0
