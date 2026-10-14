$ErrorActionPreference='Stop'
$env:FFMPEG_DIR='D:\AgentWork\sdk\ffmpeg-7.1.1-full_build-shared'
$env:PATH="$env:FFMPEG_DIR\bin;"+$env:PATH
$env:ETERNAL_HEADLESS='1';$env:ETERNAL_FPS='30'
Set-Location D:\AgentWork\ExampleApp
$evidence='D:\AgentWork\evidence'
$ffmpeg="$env:FFMPEG_DIR\bin\ffmpeg.exe"
$results=@()
foreach ($codec in @('h264_nvenc','hevc_nvenc')) {
 $p=Start-Process $ffmpeg -ArgumentList @('-hide_banner','-y','-f','lavfi','-i','ddagrab=output_idx=0:framerate=30','-frames:v','90','-c:v',$codec,'-f','null','-') -PassThru -NoNewWindow -RedirectStandardOutput "$evidence\$codec.stdout" -RedirectStandardError "$evidence\$codec.stderr"
 if (-not $p.WaitForExit(30000)) { Stop-Process -Id $p.Id; $results += "$codec timed out" } else { $results += "$codec exit=$($p.ExitCode)" }
}
$hostProcess=Start-Process '.\target\debug\eternal-host.exe' -ArgumentList '19876' -PassThru -RedirectStandardOutput "$evidence\host-smoke.stdout" -RedirectStandardError "$evidence\host-smoke.stderr"
$hostProcess.Id | Set-Content "$evidence\host-smoke.pid"
$exited=$hostProcess.WaitForExit(15000)
if ($exited) { $results += "eternal-host exited early: $($hostProcess.ExitCode)" } else { $results += 'eternal-host remained running for 15 seconds'; Stop-Process -Id $hostProcess.Id }
$hostLog="$env:APPDATA\ExampleApp\logs\eternal-host-session.log"
if (Test-Path $hostLog) { Copy-Item $hostLog "$evidence\eternal-host-hardware.log" -Force }
$results | Set-Content "$evidence\hardware-summary.txt"
