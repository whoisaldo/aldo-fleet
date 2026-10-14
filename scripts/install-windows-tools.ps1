param([string]$ToolRoot = 'D:\AgentWork\fleet-tools')

$ErrorActionPreference = 'Stop'
$source = Join-Path (Split-Path -Parent $PSScriptRoot) 'toolchains\windows'
$stateRoot = 'D:\AgentWork\fleet-state'
$record = Join-Path $stateRoot 'windows-runtime.json'
$package = Get-Content -Raw (Join-Path $source 'package.json') | ConvertFrom-Json
$codexVersion = $package.dependencies.'@openai/codex'
$claudeVersion = $package.dependencies.'@anthropic-ai/claude-code'
$codex = Join-Path $ToolRoot 'node_modules\@openai\codex-win32-x64\vendor\x86_64-pc-windows-msvc\bin\codex.exe'
$claude = Join-Path $ToolRoot 'node_modules\@anthropic-ai\claude-code-win32-x64\claude.exe'

if (Test-Path $record) {
    $previous = Get-Content -Raw $record | ConvertFrom-Json
    if ($previous.codex.version -ne $codexVersion -or $previous.claude.version -ne $claudeVersion -or $previous.codex.binary -ne $codex -or $previous.claude.binary -ne $claude) {
        throw 'Preserved the installed Fleet toolchain. New versions need a separate tool directory and an idle migration.'
    }
} else {
    New-Item -ItemType Directory -Path $ToolRoot -Force | Out-Null
    foreach ($name in @('package.json', 'package-lock.json')) {
        $from = Join-Path $source $name
        $to = Join-Path $ToolRoot $name
        if (Test-Path $to) {
            $expected = (Get-Content -Raw $from).Replace("`r`n", "`n")
            $existing = (Get-Content -Raw $to).Replace("`r`n", "`n")
            if ($expected -ne $existing) { throw "Preserved existing toolchain manifest: $to" }
        } else { Copy-Item $from $to }
    }
    if (-not (Test-Path $codex) -or -not (Test-Path $claude)) {
        Push-Location $ToolRoot
        try {
            npm.cmd ci --cache (Join-Path $stateRoot 'npm-cache') --ignore-scripts --no-audit --no-fund
            if ($LASTEXITCODE -ne 0) { throw 'Isolated toolchain installation failed.' }
        } finally { Pop-Location }
    }
}

$actualCodex = & $codex --version
if ($LASTEXITCODE -ne 0 -or $actualCodex -ne "codex-cli $codexVersion") { throw 'Unexpected Fleet Codex binary version.' }
$actualClaude = & $claude --version
if ($LASTEXITCODE -ne 0 -or $actualClaude -ne "$claudeVersion (Claude Code)") { throw 'Unexpected Fleet Claude binary version.' }
if (-not (Test-Path $record)) {
    New-Item -ItemType Directory -Path $stateRoot -Force | Out-Null
    $runtime = @{codex = @{binary = $codex; version = $codexVersion}; claude = @{binary = $claude; version = $claudeVersion}} | ConvertTo-Json -Depth 4
    [IO.File]::WriteAllText($record, $runtime, [Text.UTF8Encoding]::new($false))
}
Write-Host "Verified isolated Fleet tools: Codex $codexVersion, Claude $claudeVersion."
