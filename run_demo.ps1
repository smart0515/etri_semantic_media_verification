$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = Join-Path $projectRoot "src"

$pythonExecutable = if ($env:ETRI_PYTHON) {
    $env:ETRI_PYTHON
} else {
    (Get-Command python.exe -ErrorAction Stop).Source
}

& $pythonExecutable -m semantic_validator.cli demo `
    --annotation (Join-Path $projectRoot "samples\qvhighlights_compatible_sample.jsonl") `
    --extension (Join-Path $projectRoot "samples\etri_semantic_extension_sample.jsonl") `
    --output-dir (Join-Path $projectRoot "artifacts\demo")

if ($LASTEXITCODE -ne 0) {
    throw "Demo verification failed with exit code $LASTEXITCODE"
}

Write-Host "Verification artifacts: $projectRoot\artifacts\demo"
