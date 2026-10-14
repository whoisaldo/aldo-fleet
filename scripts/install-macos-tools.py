#!/usr/bin/env python3
"""Install the pinned fleet CLIs without replacing native macOS CLI installs."""
import os
from pathlib import Path
import shutil
import subprocess
import sys

from fleetlib import ROOT, atomic_write, encode, read_json, state_dir


def main():
    if sys.platform != "darwin":
        raise ValueError("Use the Windows tool installer on Windows")
    state = state_dir(read_json(ROOT / "fleet.json"))
    target = state / "tools/macos"
    target.mkdir(parents=True, exist_ok=True)
    for name in ("package.json", "package-lock.json"):
        source = ROOT / "toolchains/macos" / name
        dest = target / name
        if dest.exists() and read_json(dest) != read_json(source):
            raise ValueError("Existing toolchain manifest differs; preserve it and use a new tool directory")
        if not dest.exists():
            shutil.copy2(source, dest)
    arch = "arm64" if os.uname().machine == "arm64" else "x64"
    modules = target / "node_modules"
    codex = list(modules.glob(f"@openai/codex-darwin-{arch}/**/bin/codex"))
    claude = modules / f"@anthropic-ai/claude-code-darwin-{arch}/claude"
    if not codex or not claude.exists():
        if modules.exists():
            raise ValueError("Incomplete existing toolchain; inspect it before replacing files")
        env = dict(os.environ)
        env["PATH"] = "/opt/homebrew/bin:/usr/local/bin:" + env.get("PATH", "")
        npm = shutil.which("npm", path=env["PATH"])
        if not npm:
            raise ValueError("Node and npm are required")
        subprocess.run([npm, "ci", "--ignore-scripts", "--no-audit", "--no-fund", "--cache", str(state / "npm-cache")], cwd=target, env=env, check=True)
        codex = list(modules.glob(f"@openai/codex-darwin-{arch}/**/bin/codex"))
    binaries = {"codex": codex[0], "claude": claude}
    runtime = {}
    expected = {"codex": "0.160.0", "claude": "2.1.289"}
    for name, binary in binaries.items():
        version = subprocess.check_output([str(binary), "--version"], text=True).strip()
        if expected[name] not in version.split():
            raise ValueError(f"Unexpected {name} version: {version}")
        runtime[name] = {"binary": str(binary), "version": version}
        print(name, version)
    path = state / "toolchain-runtime.json"
    if path.exists() and read_json(path) != runtime:
        raise ValueError("Existing runtime selection differs; preserved it")
    atomic_write(path, encode(runtime))


if __name__ == "__main__":
    main()
