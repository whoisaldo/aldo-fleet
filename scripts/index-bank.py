#!/usr/bin/env python3
"""Hash reviewed, staged source files. Inspect the Git diff before running this."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    dirty = subprocess.check_output(['git', 'diff', '--name-only'], cwd=ROOT).decode().splitlines()
    dirty = [name for name in dirty if name != 'bank/files.json']
    if dirty:
        raise ValueError('Stage reviewed changes before indexing: ' + ', '.join(dirty))
    names = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    result = {}
    for name in sorted(n for n in names if n and n != 'bank/files.json'):
        path = ROOT / name
        if path.is_symlink() or not path.resolve().is_relative_to(ROOT.resolve()):
            raise ValueError(f'Review symlink before sharing: {name}')
        if path.is_file():
            result[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    (ROOT / 'bank/files.json').write_text(json.dumps(result, indent=2) + '\n')
    print(f'Indexed {len(result)} reviewed source files. Review and stage bank/files.json too.')


if __name__ == '__main__':
    main()
