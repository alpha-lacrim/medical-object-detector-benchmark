$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
$benchmarkPython = "C:\Users\Pouyan\.conda\envs\torch-gpu\python.exe"
$trainingStatePath = Join-Path $PSScriptRoot "training_state.json"
$statePath = Join-Path $PSScriptRoot "downstream_state.json"
$robustnessTable = Join-Path $projectRoot "results\tables\statistical_robustness_comparison.csv"
$phase6Summary = Join-Path $projectRoot "results\logs\phase6_robustness\summary.json"

$state = [ordered]@{
    status = "waiting_for_training"
    started_at = (Get-Date).ToUniversalTime().ToString("o")
    completed_at = $null
    active_step = $null
    robustness_table_sha256_before = (Get-FileHash -LiteralPath $robustnessTable -Algorithm SHA256).Hash.ToLowerInvariant()
    robustness_table_sha256_after = $null
    phase6_summary_sha256_before = (Get-FileHash -LiteralPath $phase6Summary -Algorithm SHA256).Hash.ToLowerInvariant()
    phase6_summary_sha256_after = $null
    steps = @()
}

function Write-State {
    $state | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $statePath -Encoding UTF8
}

function Invoke-Step {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string[]]$Arguments
    )
    $record = [ordered]@{
        name = $Name
        status = "running"
        started_at = (Get-Date).ToUniversalTime().ToString("o")
        completed_at = $null
        exit_code = $null
        stdout = (Join-Path $PSScriptRoot ($Name + ".out"))
        stderr = (Join-Path $PSScriptRoot ($Name + ".err"))
    }
    $state.status = "running"
    $state.active_step = $Name
    $state.steps += $record
    Write-State
    $process = Start-Process `
        -FilePath $benchmarkPython `
        -ArgumentList $Arguments `
        -WorkingDirectory $projectRoot `
        -RedirectStandardOutput $record.stdout `
        -RedirectStandardError $record.stderr `
        -WindowStyle Hidden `
        -Wait `
        -PassThru
    $record.exit_code = $process.ExitCode
    $record.completed_at = (Get-Date).ToUniversalTime().ToString("o")
    if ($process.ExitCode -ne 0) {
        $record.status = "failed"
        $state.status = "failed"
        $state.active_step = $null
        $state.completed_at = $record.completed_at
        Write-State
        exit $process.ExitCode
    }
    $record.status = "complete"
    Write-State
}

Write-State
while ($true) {
    if (-not (Test-Path -LiteralPath $trainingStatePath)) {
        Start-Sleep -Seconds 30
        continue
    }
    $trainingState = Get-Content -Raw -LiteralPath $trainingStatePath | ConvertFrom-Json
    if ($trainingState.status -eq "failed") {
        $state.status = "blocked_by_training_failure"
        $state.completed_at = (Get-Date).ToUniversalTime().ToString("o")
        Write-State
        exit 1
    }
    if ($trainingState.status -eq "complete") {
        break
    }
    Start-Sleep -Seconds 30
}

Invoke-Step -Name "evaluation_preflight" -Arguments @(
    "-m", "src.evaluate", "--config", "configs/evaluation.yaml", "--mode", "preflight"
)
Invoke-Step -Name "evaluation_n5" -Arguments @(
    "-m", "src.evaluate", "--config", "configs/evaluation.yaml", "--mode", "evaluate"
)
Invoke-Step -Name "statistics_preflight" -Arguments @(
    "-m", "src.stats.run_statistics", "--config", "configs/statistics.yaml", "--mode", "preflight"
)
Invoke-Step -Name "statistics_clean_n5" -Arguments @(
    "-m", "src.stats.run_statistics", "--config", "configs/statistics.yaml", "--mode", "run", "--scope", "clean"
)

$state.robustness_table_sha256_after = (Get-FileHash -LiteralPath $robustnessTable -Algorithm SHA256).Hash.ToLowerInvariant()
$state.phase6_summary_sha256_after = (Get-FileHash -LiteralPath $phase6Summary -Algorithm SHA256).Hash.ToLowerInvariant()
if ($state.robustness_table_sha256_after -ne $state.robustness_table_sha256_before) {
    $state.status = "failed_integrity_check"
    $state.completed_at = (Get-Date).ToUniversalTime().ToString("o")
    Write-State
    throw "clean-only statistics changed the robustness table"
}
if ($state.phase6_summary_sha256_after -ne $state.phase6_summary_sha256_before) {
    $state.status = "failed_integrity_check"
    $state.completed_at = (Get-Date).ToUniversalTime().ToString("o")
    Write-State
    throw "Batch 16 changed the Phase 6 summary"
}
$state.status = "complete"
$state.active_step = $null
$state.completed_at = (Get-Date).ToUniversalTime().ToString("o")
Write-State
