$ErrorActionPreference='Stop'
$ProgressPreference='SilentlyContinue'
Stop-ScheduledTask -TaskName Fleet-T3Code
$listener=Get-NetTCPConnection -State Listen -LocalPort 3773 -ErrorAction SilentlyContinue
if ($listener) {
 $p=Get-Process -Id $listener.OwningProcess
 if ($p.Path -ne "$env:USERPROFILE\.t3\runtime\versions\0.0.42\t3.exe") { throw 'Unexpected listener on 3773; stop relocation.' }
 Stop-Process -Id $p.Id
}
$items=@(
 @("$env:USERPROFILE\.t3",'D:\AgentWork\profiles\t3'),
 @("$env:LOCALAPPDATA\cursor-agent",'D:\AgentWork\tools\cursor-agent'),
 @("$env:USERPROFILE\agent-skills",'D:\AgentWork\skills\shared'),
 @("$env:USERPROFILE\.agents\skills",'D:\AgentWork\skills\agents'),
 @("$env:USERPROFILE\.codex\skills",'D:\AgentWork\skills\codex'),
 @("$env:USERPROFILE\.codex_work\skills",'D:\AgentWork\skills\codex-work'),
 @("$env:USERPROFILE\.cursor\skills",'D:\AgentWork\skills\cursor'),
 @("$env:USERPROFILE\.cursor\skills-cursor",'D:\AgentWork\skills\cursor-builtins'),
 @("$env:USERPROFILE\.claude\skills",'D:\AgentWork\skills\claude'),
 @("$env:USERPROFILE\.claude_secondary\skills",'D:\AgentWork\skills\claude-secondary')
)
foreach ($item in $items) {
 $source=$item[0];$destination=$item[1]
 if (-not (Test-Path $source)) { continue }
 if ((Get-Item -Force $source).Attributes -band [IO.FileAttributes]::ReparsePoint) { continue }
 New-Item -ItemType Directory -Force $destination | Out-Null
 robocopy.exe $source $destination /E /MOVE /R:1 /W:1 /XJ /NFL /NDL /NJH /NJS | Out-Null
 if ($LASTEXITCODE -ge 8) { throw "Relocation failed for $source; files are preserved in source/destination." }
 if (Test-Path $source) { Remove-Item -LiteralPath $source -Force }
 cmd.exe /c "mklink /J `"$source`" `"$destination`"" | Out-Null
 if ($LASTEXITCODE -ne 0) { throw "Junction creation failed for $source" }
 Write-Output "Moved $source to $destination"
}
Start-ScheduledTask -TaskName Fleet-T3Code
Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'" | Select @{n='FreeGB';e={[math]::Round($_.FreeSpace/1GB,2)}}
