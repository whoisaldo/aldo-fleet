param(
    [string]$Archive = (Join-Path $PSScriptRoot 'agent-configs.zip'),
    [string]$Manifest = (Join-Path $PSScriptRoot 'manifest.json')
)
$ErrorActionPreference = 'Stop'
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$destinationHome = $env:USERPROFILE
$backup = Join-Path $destinationHome "agent-migration-backups\$stamp"
$unpack = Join-Path $env:TEMP "agent-config-import-$stamp"
New-Item -ItemType Directory -Force $backup, $unpack | Out-Null
Expand-Archive -LiteralPath $Archive -DestinationPath $unpack
$entries = Get-Content -Raw $Manifest | ConvertFrom-Json
# Verify the complete payload before changing any destination file.
foreach ($entry in $entries) {
    $source = Join-Path $unpack $entry.path
    if ((Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash -ne $entry.sha256) {
        throw "Payload hash mismatch: $($entry.path)"
    }
}
foreach ($entry in $entries) {
    $source = Join-Path $unpack $entry.path
    $destination = Join-Path $destinationHome $entry.path
    if (Test-Path -LiteralPath $destination) {
        $saved = Join-Path $backup $entry.path
        New-Item -ItemType Directory -Force (Split-Path $saved) | Out-Null
        Copy-Item -LiteralPath $destination -Destination $saved
    }
    New-Item -ItemType Directory -Force (Split-Path $destination) | Out-Null
    Copy-Item -LiteralPath $source -Destination $destination -Force
}
# Resolve T3 home paths against this Windows account, preserving profile separation.
$t3Settings = Join-Path $destinationHome '.t3\userdata\settings.json'
$settings = Get-Content -Raw $t3Settings | ConvertFrom-Json
foreach ($instance in $settings.providerInstances.PSObject.Properties) {
    if ($instance.Value.config.homePath -like '~/*') {
        $instance.Value.config.homePath = Join-Path $destinationHome $instance.Value.config.homePath.Substring(2)
    }
}
[IO.File]::WriteAllText($t3Settings, ($settings | ConvertTo-Json -Depth 50), (New-Object Text.UTF8Encoding($false)))
$bin = Join-Path $destinationHome '.local\bin'
New-Item -ItemType Directory -Force $bin | Out-Null
foreach ($profile in @('personal', 'work')) {
    $codexHome = if ($profile -eq 'personal') { '.codex' } else { '.codex_work' }
    $wrapper = Join-Path $bin "codex-$profile.cmd"
    if (Test-Path $wrapper) {
        Copy-Item $wrapper (Join-Path $backup "codex-$profile.cmd")
    }
    $lines = @('@echo off', 'setlocal', "set `"CODEX_HOME=%USERPROFILE%\$codexHome`"", 'call codex %*', 'exit /b %errorlevel%')
    [IO.File]::WriteAllLines($wrapper, $lines, [Text.Encoding]::ASCII)
}
Write-Host "Imported $($entries.Count) files. Existing files backed up in $backup"
Write-Host "Personal launcher: $bin\codex-personal.cmd"
Write-Host "Work launcher: $bin\codex-work.cmd"
Write-Host 'Provider executables and authentication must be verified separately.'
