$ErrorActionPreference='Stop'
$env:PATH="$env:USERPROFILE\.local\bin;$env:LOCALAPPDATA\cursor-agent;$env:APPDATA\npm;$env:USERPROFILE\.cargo\bin;C:\Program Files\Git\cmd;C:\Program Files\nodejs;"+$env:PATH
$env:FFMPEG_DIR='D:\AgentWork\sdk\ffmpeg-7.1.1-full_build-shared'
$env:LIBCLANG_PATH='D:\AgentWork\LLVM\bin'
$env:CARGO_HOME='D:\AgentWork\cargo'
$env:TEMP='D:\AgentWork\temp';$env:TMP=$env:TEMP
$env:PATH="$env:FFMPEG_DIR\bin;"+$env:PATH
$vsRoot='C:\Program Files\Microsoft Visual Studio\2022\Community'
Import-Module "$vsRoot\Common7\Tools\Microsoft.VisualStudio.DevShell.dll"
Enter-VsDevShell -VsInstallPath $vsRoot -SkipAutomaticLocation -DevCmdArguments '-arch=x64 -host_arch=x64'
$env:BINDGEN_EXTRA_CLANG_ARGS = (($env:INCLUDE -split ';' | Where-Object { $_ } | ForEach-Object { '-isystem "' + $_ + '"' }) -join ' ')
Set-Location D:\AgentWork\ExampleApp
& "$env:USERPROFILE\.local\bin\t3.cmd" serve --host 0.0.0.0 --port 3773 --no-browser --auto-bootstrap-project-from-cwd *> D:\AgentWork\evidence\t3-server.log
exit $LASTEXITCODE
