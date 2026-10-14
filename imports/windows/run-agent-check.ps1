$ProgressPreference='SilentlyContinue'
$env:CODEX_HOME="$env:USERPROFILE\.codex"
$env:PATH="$env:USERPROFILE\.local\bin;$env:APPDATA\npm;$env:USERPROFILE\.cargo\bin;C:\Program Files\Git\cmd;"+$env:PATH
Set-Location D:\AgentWork\ExampleApp
& "$env:APPDATA\npm\codex.cmd" exec --sandbox workspace-write --json -o D:\AgentWork\evidence\interactive-agent.md 'Run hostname and rustc -vV with your shell tool. Then read the first 20 lines of HARDWARE_VERIFICATION.md. Report the machine name, Rust target and one hardware test from that file. Do not modify project files, start builds or read auth files. If shell execution fails, report the error and stop.' > D:\AgentWork\evidence\interactive-agent.jsonl 2> D:\AgentWork\evidence\interactive-agent.stderr
$LASTEXITCODE | Set-Content D:\AgentWork\evidence\interactive-agent.exit
