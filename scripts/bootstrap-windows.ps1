param(
    [Parameter(Mandatory = $true)][string]$ReleaseArchive,
    [Parameter(Mandatory = $true)][string]$Sha256,
    [Parameter(Mandatory = $true)][string]$GatewayKeyDirectory,
    [ValidateSet('fleet-codex', 'fleet-claude', 'fleet-secondary')]
    [string[]]$Profiles = @('fleet-codex'),
    [string]$PythonExe = 'python'
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$stateRoot = 'D:\AgentWork\fleet-state'
$binRoot = 'D:\AgentWork\bin'
$priorState = $env:FLEET_STATE_DIR
$pythonPath = (Get-Command $PythonExe -ErrorAction Stop).Source
$version = & $pythonPath -c 'import sys; print(int(sys.version_info >= (3,11)))'
if ($LASTEXITCODE -ne 0 -or $version -ne '1') { throw 'Python 3.11 or newer is required.' }
if (-not (Test-Path 'D:\AgentWork')) { throw 'Expected mainpc work root D:\AgentWork.' }

function Protect-PrivatePath([string]$Path) {
    $principal = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
    & icacls.exe $Path '/inheritance:r' '/grant:r' "${principal}:(OI)(CI)F" | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Cannot restrict permissions: $Path" }
}

function Write-NewOrIdentical([string]$Path, [string]$Content) {
    if (Test-Path $Path) {
        if ([System.IO.File]::ReadAllText($Path) -ne $Content) {
            throw "Preserving an existing file with different contents: $Path"
        }
    } else {
        [System.IO.File]::WriteAllText($Path, $Content, [System.Text.UTF8Encoding]::new($false))
    }
}

# Resolve the required key files before changing local state.
$identities = @{}
foreach ($profile in $Profiles) {
    $identity = if ($profile -eq 'fleet-secondary') { 'secondary' } else { 'personal' }
    $source = Join-Path $GatewayKeyDirectory ($identity + '.json')
    $key = Get-Content -Raw $source | ConvertFrom-Json
    if (-not $key.api_key -or $key.api_key.Length -lt 30) { throw "Missing client key for $identity" }
    if ($key.management_key) { throw 'Copy only client keys to Windows, never gateway management credentials.' }
    $identities[$identity] = $key.api_key
}

try {
    $env:FLEET_STATE_DIR = $stateRoot
    New-Item -ItemType Directory -Path $stateRoot -Force | Out-Null
    Protect-PrivatePath $stateRoot
    & (Join-Path $PSScriptRoot 'install-windows-tools.ps1')
    & $pythonPath (Join-Path $PSScriptRoot 'portable.py') install --archive $ReleaseArchive --sha256 $Sha256
    if ($LASTEXITCODE -ne 0) { throw 'Skill release verification failed.' }
    $keyRoot = Join-Path $stateRoot 'gateway-keys'
    New-Item -ItemType Directory -Path $keyRoot -Force | Out-Null
    foreach ($identity in $identities.Keys) {
        $destination = Join-Path $keyRoot ($identity + '.json')
        $content = @{api_key = $identities[$identity]} | ConvertTo-Json
        if (Test-Path $destination) {
            $existing = Get-Content -Raw $destination | ConvertFrom-Json
            if ($existing.api_key -ne $identities[$identity]) { throw "Preserved an existing $identity client key." }
        } else {
            [System.IO.File]::WriteAllText($destination, $content, [System.Text.UTF8Encoding]::new($false))
        }
    }
    foreach ($profile in $Profiles) {
        $record = Join-Path $stateRoot "profiles\$profile\.fleet-profile.json"
        if (Test-Path $record) {
            Write-Host "Preserved installed profile $profile; doctor will verify its pinned release."
        } else {
            & $pythonPath (Join-Path $PSScriptRoot 'fleetlib.py') apply --profile $profile
            if ($LASTEXITCODE -ne 0) { throw "Profile installation failed: $profile" }
        }
    }
    New-Item -ItemType Directory -Path $binRoot -Force | Out-Null
    $entrypoint = Join-Path $PSScriptRoot 'fleetlib.py'
    $launcher = '@echo off' + "`r`n" + '"' + $pythonPath + '" "' + $entrypoint + '" %*' + "`r`n"
    Write-NewOrIdentical (Join-Path $binRoot 'fleet.cmd') $launcher
    $names = @{'fleet-codex' = 'codex-fleet'; 'fleet-claude' = 'claude-fleet'; 'fleet-secondary' = 'claude-secondary-fleet'}
    foreach ($profile in $Profiles) {
        $launcher = '@echo off' + "`r`n" + '"' + $pythonPath + '" "' + $entrypoint + '" run --profile ' + $profile + ' -- %*' + "`r`n"
        Write-NewOrIdentical (Join-Path $binRoot ($names[$profile] + '.cmd')) $launcher
    }
    $doctorArgs = @('doctor')
    foreach ($profile in $Profiles) { $doctorArgs += @('--profile', $profile) }
    & $pythonPath $entrypoint @doctorArgs
    if ($LASTEXITCODE -ne 0) { throw 'Fleet doctor has pending checks.' }
    Write-Host "Installed additive launchers in $binRoot. Start only new conversations with them."
    Write-Host 'Windows T3 provider registration still requires a live audit and its supported settings API.'
} finally {
    $env:FLEET_STATE_DIR = $priorState
}
