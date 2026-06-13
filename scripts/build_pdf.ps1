$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $ScriptDir
$PaperDir = Join-Path $Root "paper"
$DataDir = Join-Path $Root "data"
$DownloadsPdf = "C:\Users\wangz\Downloads\43.pdf"
$LocalPdf = Join-Path $PaperDir "main.pdf"
$BuildStatus = Join-Path $DataDir "build_status.json"

New-Item -ItemType Directory -Force -Path $DataDir | Out-Null

Push-Location $PaperDir
try {
    pdflatex -interaction=nonstopmode -halt-on-error main.tex | Out-Host
    bibtex main | Out-Host
    foreach ($pass in 1..3) {
        pdflatex -interaction=nonstopmode -halt-on-error main.tex | Out-Host
    }

    if (-not (Test-Path -LiteralPath $LocalPdf)) {
        throw "Expected PDF was not produced: $LocalPdf"
    }

    Copy-Item -LiteralPath $LocalPdf -Destination $DownloadsPdf -Force
    Remove-Item -LiteralPath $LocalPdf -Force

    $status = [ordered]@{
        paper = 43
        decision = "workshop-only"
        canonical_pdf = $DownloadsPdf
        local_pdf_removed = -not (Test-Path -LiteralPath $LocalPdf)
        built_at = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss zzz")
    }

    $status | ConvertTo-Json | Set-Content -Path $BuildStatus -Encoding UTF8
}
finally {
    Pop-Location
}
