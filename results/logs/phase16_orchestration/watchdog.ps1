$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$trainingStatePath = Join-Path $PSScriptRoot "training_state.json"
$downstreamStatePath = Join-Path $PSScriptRoot "downstream_state.json"
$healthStatePath = Join-Path $PSScriptRoot "health_state.json"
$samplesPath = Join-Path $PSScriptRoot "health_samples.jsonl"
$staleThresholdMinutes = 20
$temperatureAlertCelsius = 85

while ($true) {
    $now = (Get-Date).ToUniversalTime()
    $training = Get-Content -Raw -LiteralPath $trainingStatePath | ConvertFrom-Json
    $downstream = Get-Content -Raw -LiteralPath $downstreamStatePath | ConvertFrom-Json
    $activeName = if ($training.status -eq "running") {
        [string]$training.active_job
    } else {
        [string]$downstream.active_step
    }
    $activeLog = if ($activeName) {
        Join-Path $PSScriptRoot ($activeName + ".out")
    } else {
        $null
    }
    $logAgeMinutes = if ($activeLog -and (Test-Path -LiteralPath $activeLog)) {
        ($now - (Get-Item -LiteralPath $activeLog).LastWriteTimeUtc).TotalMinutes
    } else {
        $null
    }
    $pythonProcesses = @(Get-Process python -ErrorAction SilentlyContinue)
    $gpuParts = @(
        nvidia-smi `
            --query-gpu=utilization.gpu,memory.used,memory.free,temperature.gpu,pstate `
            --format=csv,noheader,nounits
    )[0].Split(",") | ForEach-Object { $_.Trim() }
    $alerts = @()
    if ($training.status -eq "running" -and $pythonProcesses.Count -eq 0) {
        $alerts += "training state is running but no Python process exists"
    }
    if ($null -ne $logAgeMinutes -and $logAgeMinutes -gt $staleThresholdMinutes) {
        $alerts += "active stdout has not changed for more than $staleThresholdMinutes minutes"
    }
    if ([int]$gpuParts[3] -ge $temperatureAlertCelsius) {
        $alerts += "GPU temperature reached the configured alert threshold"
    }
    if ($training.status -in @("failed", "blocked_by_training_failure")) {
        $alerts += "training queue reported failure"
    }
    if ($downstream.status -in @("failed", "failed_integrity_check", "blocked_by_training_failure")) {
        $alerts += "downstream queue reported failure"
    }
    $sample = [ordered]@{
        timestamp = $now.ToString("o")
        status = if ($alerts.Count -eq 0) { "healthy" } else { "alert" }
        alerts = $alerts
        training_status = $training.status
        downstream_status = $downstream.status
        active_name = $activeName
        active_log_age_minutes = if ($null -eq $logAgeMinutes) { $null } else { [math]::Round($logAgeMinutes, 2) }
        python_process_count = $pythonProcesses.Count
        gpu_utilization_percent = [int]$gpuParts[0]
        gpu_memory_used_mib = [int]$gpuParts[1]
        gpu_memory_free_mib = [int]$gpuParts[2]
        gpu_temperature_celsius = [int]$gpuParts[3]
        gpu_pstate = $gpuParts[4]
    }
    $sample | ConvertTo-Json -Compress | Add-Content -LiteralPath $samplesPath -Encoding UTF8
    $sample | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $healthStatePath -Encoding UTF8

    if ($training.status -eq "failed" -or $downstream.status -in @(
        "complete", "failed", "failed_integrity_check", "blocked_by_training_failure"
    )) {
        break
    }
    Start-Sleep -Seconds 60
}
