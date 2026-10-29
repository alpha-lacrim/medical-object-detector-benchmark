$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
$benchmarkPython = "C:\Users\Pouyan\.conda\envs\torch-gpu\python.exe"
$statePath = Join-Path $PSScriptRoot "training_state.json"

$jobs = @(
    @{
        Name = "faster_rcnn_seed271"
        Arguments = @(
            "-m", "src.models.train_faster_rcnn",
            "--config", "configs/faster_rcnn_seed271.yaml",
            "--mode", "train",
            "--approved-benchmark", "results/logs/faster_rcnn_rsna_seed271_benchmark/benchmark_estimate.json"
        )
    },
    @{
        Name = "faster_rcnn_seed314"
        Arguments = @(
            "-m", "src.models.train_faster_rcnn",
            "--config", "configs/faster_rcnn_seed314.yaml",
            "--mode", "train",
            "--approved-benchmark", "results/logs/faster_rcnn_rsna_seed314_benchmark/benchmark_estimate.json"
        )
    },
    @{
        Name = "yolo11s_seed271"
        Arguments = @(
            "-m", "src.models.train_yolo",
            "--config", "configs/yolo_seed271.yaml",
            "--mode", "train"
        )
    },
    @{
        Name = "yolo11s_seed314"
        Arguments = @(
            "-m", "src.models.train_yolo",
            "--config", "configs/yolo_seed314.yaml",
            "--mode", "train"
        )
    }
)

$state = [ordered]@{
    status = "running"
    started_at = (Get-Date).ToUniversalTime().ToString("o")
    completed_at = $null
    active_job = $null
    jobs = @()
}

function Write-State {
    $state | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $statePath -Encoding UTF8
}

foreach ($job in $jobs) {
    $record = [ordered]@{
        name = $job.Name
        status = "running"
        started_at = (Get-Date).ToUniversalTime().ToString("o")
        completed_at = $null
        exit_code = $null
        stdout = (Join-Path $PSScriptRoot ($job.Name + ".out"))
        stderr = (Join-Path $PSScriptRoot ($job.Name + ".err"))
    }
    $state.active_job = $job.Name
    $state.jobs += $record
    Write-State

    $process = Start-Process `
        -FilePath $benchmarkPython `
        -ArgumentList $job.Arguments `
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
        $state.active_job = $null
        $state.completed_at = $record.completed_at
        Write-State
        exit $process.ExitCode
    }
    $record.status = "complete"
    Write-State
}

$state.status = "complete"
$state.active_job = $null
$state.completed_at = (Get-Date).ToUniversalTime().ToString("o")
Write-State
