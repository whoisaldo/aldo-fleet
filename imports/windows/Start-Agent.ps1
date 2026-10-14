param(
 [Parameter(Mandatory=$true)][string]$Prompt,
 [ValidateSet('personal','work','cursor')][string]$Profile='personal',
 [string]$Workspace='D:\AgentWork\ExampleApp'
)
$ErrorActionPreference='Stop'
$jobId=(Get-Date -Format 'yyyyMMdd-HHmmss')+'-'+[guid]::NewGuid().ToString('N').Substring(0,6)
$job="D:\AgentWork\jobs\$jobId"
New-Item -ItemType Directory -Force $job | Out-Null
[IO.File]::WriteAllText("$job\prompt.txt",$Prompt,(New-Object Text.UTF8Encoding($false)))
@{profile=$Profile;workspace=$Workspace;job=$job} | ConvertTo-Json | Set-Content "$job\job.json"
$runner=@'
param([string]$Job)
$ProgressPreference='SilentlyContinue'
$j=Get-Content -Raw "$Job\job.json" | ConvertFrom-Json
$env:PATH="$env:USERPROFILE\.local\bin;$env:LOCALAPPDATA\cursor-agent;$env:APPDATA\npm;$env:USERPROFILE\.cargo\bin;C:\Program Files\Git\cmd;"+$env:PATH
$env:FFMPEG_DIR='D:\AgentWork\sdk\ffmpeg-7.1.1-full_build-shared'
$env:LIBCLANG_PATH='D:\AgentWork\LLVM\bin'
$env:CARGO_HOME='D:\AgentWork\cargo'
$env:TEMP='D:\AgentWork\temp';$env:TMP=$env:TEMP
$env:PATH="$env:FFMPEG_DIR\bin;"+$env:PATH
$vs='C:\Program Files\Microsoft Visual Studio\2022\Community'
Import-Module "$vs\Common7\Tools\Microsoft.VisualStudio.DevShell.dll"
Enter-VsDevShell -VsInstallPath $vs -SkipAutomaticLocation -DevCmdArguments '-arch=x64 -host_arch=x64'
$env:BINDGEN_EXTRA_CLANG_ARGS=(($env:INCLUDE -split ';' | Where-Object {$_} | ForEach-Object {'-isystem "'+$_+'"'}) -join ' ')
Set-Location $j.workspace
$prompt=Get-Content -Raw "$Job\prompt.txt"
if ($j.profile -eq 'cursor') {
 & "$env:LOCALAPPDATA\cursor-agent\agent.cmd" --trust -p $prompt > "$Job\result.md" 2> "$Job\stderr.log"
} else {
 $env:CODEX_HOME=if ($j.profile -eq 'work') {"$env:USERPROFILE\.codex_work"} else {"$env:USERPROFILE\.codex"}
 & "$env:APPDATA\npm\node_modules\@openai\codex\node_modules\@openai\codex-win32-x64\vendor\x86_64-pc-windows-msvc\bin\codex.exe" exec --sandbox workspace-write --json -o "$Job\result.md" $prompt > "$Job\events.jsonl" 2> "$Job\stderr.log"
}
$LASTEXITCODE | Set-Content "$Job\exit-code.txt"
'@
[IO.File]::WriteAllText("$job\run.ps1",$runner,(New-Object Text.UTF8Encoding($false)))
$user=[Security.Principal.WindowsIdentity]::GetCurrent().Name
$action=New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$job\run.ps1`" -Job `"$job`"" -WorkingDirectory $Workspace
$principal=New-ScheduledTaskPrincipal -UserId $user -LogonType Interactive -RunLevel Limited
$settings=New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Hours 8) -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$name="Fleet-Agent-$jobId"
Register-ScheduledTask -TaskName $name -Action $action -Principal $principal -Settings $settings | Out-Null
Start-ScheduledTask -TaskName $name
Write-Output "Task: $name"
Write-Output "Results: $job"
Write-Output 'This job runs in the logged-in Windows session and survives SSH disconnection.'
