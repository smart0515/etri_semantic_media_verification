$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = Join-Path $projectRoot "src"

$pythonExecutable = if ($env:ETRI_PYTHON) {
    $env:ETRI_PYTHON
} else {
    (Get-Command python.exe -ErrorAction Stop).Source
}

& $pythonExecutable -m unittest discover -s (Join-Path $projectRoot "tests") -v
if ($LASTEXITCODE -ne 0) {
    throw "Tests failed with exit code $LASTEXITCODE"
}
