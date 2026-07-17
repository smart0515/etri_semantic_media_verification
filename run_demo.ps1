$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = Join-Path $projectRoot "src"

python -m semantic_validator.cli demo `
    --annotation (Join-Path $projectRoot "samples\qvhighlights_compatible_sample.jsonl") `
    --extension (Join-Path $projectRoot "samples\etri_semantic_extension_sample.jsonl") `
    --output-dir (Join-Path $projectRoot "artifacts\demo")

Write-Host "Verification artifacts: $projectRoot\artifacts\demo"
