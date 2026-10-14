$ErrorActionPreference='Stop'
$ProgressPreference='SilentlyContinue'
$env:FFMPEG_DIR='D:\AgentWork\sdk\ffmpeg-7.1.1-full_build-shared'
$env:LIBCLANG_PATH='D:\AgentWork\LLVM\bin'
$env:CARGO_HOME='D:\AgentWork\cargo'
$env:CARGO_TARGET_DIR='D:\AgentWork\ExampleApp\target'
$env:TEMP='D:\AgentWork\temp'; $env:TMP=$env:TEMP
$env:PATH="$env:FFMPEG_DIR\bin;$env:USERPROFILE\.cargo\bin;"+$env:PATH
$vsRoot='C:\Program Files\Microsoft Visual Studio\2022\Community'
Import-Module "$vsRoot\Common7\Tools\Microsoft.VisualStudio.DevShell.dll"
Enter-VsDevShell -VsInstallPath $vsRoot -SkipAutomaticLocation -DevCmdArguments '-arch=x64 -host_arch=x64'
$env:BINDGEN_EXTRA_CLANG_ARGS = (($env:INCLUDE -split ';' | Where-Object { $_ } | ForEach-Object { '-isystem "' + $_ + '"' }) -join ' ')
Set-Location D:\AgentWork\ExampleApp
New-Item -ItemType Directory -Force D:\AgentWork\evidence | Out-Null
Start-Transcript -Path D:\AgentWork\evidence\cargo-build-test.txt -Force
try {
 cargo build --workspace --locked
 if ($LASTEXITCODE -ne 0) { throw 'cargo build failed' }
 cargo test --workspace --locked
 if ($LASTEXITCODE -ne 0) { throw 'cargo test failed' }
} finally { Stop-Transcript }
