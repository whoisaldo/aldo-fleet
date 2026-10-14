$ErrorActionPreference='Stop'
$env:PATH='D:\AgentWork\sdk\ffmpeg-7.1.1-full_build-shared\bin;'+$env:PATH
$env:ETERNAL_HEADLESS='1';$env:ETERNAL_FPS='30';$env:ETERNAL_ENCODER='hevc_nvenc'
Set-Location D:\AgentWork\ExampleApp
$results=@()
foreach ($mode in @('hevc')) {
 $env:ETERNAL_HEVC=if ($mode -eq 'hevc') { '1' } else { '0' }
 $prefix="D:\AgentWork\evidence\host-nvenc-$mode"
 $p=Start-Process '.\target\debug\eternal-host.exe' -ArgumentList '19876' -PassThru -RedirectStandardOutput "$prefix.stdout" -RedirectStandardError "$prefix.stderr"
 $p.Id | Set-Content "$prefix.pid"
 if ($p.WaitForExit(20000)) { $results += "$mode exited early: $($p.ExitCode)" } else { Stop-Process -Id $p.Id; $results += "$mode ran for 20 seconds" }
 Copy-Item "$env:APPDATA\ExampleApp\logs\eternal-host-session.log" "$prefix.log" -Force
}
$results | Set-Content D:\AgentWork\evidence\host-nvenc-summary.txt
