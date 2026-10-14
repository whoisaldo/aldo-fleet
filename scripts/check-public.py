#!/usr/bin/env python3
"""Check tracked public source; report locations without printing matched values."""
import argparse
import hashlib
import ipaddress
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER_USERS = {'your-user', 'example', 'example-user', 'username', 'USER', 'YOU', '...'}
PRIVATE_NAMES = {'auth.json', '.credentials.json', 'credentials.json', 'cookies.json',
                 't3-session.json', 'server-runtime.json', 'bank-selection.local.json'}
PRIVATE_SUFFIXES = {'.pem', '.key', '.sqlite', '.sqlite3', '.db', '.xlsx', '.log', '.zip'}
UUID = re.compile(r'\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b', re.I)
MAC_HOME = re.compile(r'/' r'Users/([^/\s\x22\x27`<>]+)')
WIN_HOME = re.compile(r'[A-Z]:\\+Users\\+([^\\\s\x22\x27`<>]+)', re.I)
TAILNET = re.compile(r'\b(?:[a-z0-9-]+\.)+ts\.net\b', re.I)
TAIL_IP = re.compile(r'\b100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.\d{1,3}\.\d{1,3}\b')


def findings(name, data):
    """Supplement Gitleaks with public-repo privacy and state-file checks."""
    result = []
    path = PurePosixPath(name)
    if (path.name in PRIVATE_NAMES or path.suffix.lower() in PRIVATE_SUFFIXES
            or path.name == '.env' or path.name.startswith('.env.') and not path.name.endswith('.example')
            or name.endswith('/canvas-planning/config.json')
            or any(part in {'.t3', '.openclaw', 'sessions', 'backups'} for part in path.parts)):
        result.append(('private-state-file', name, 0))
    text = data.decode('utf-8', errors='ignore')
    for number, line in enumerate(text.splitlines(), 1):
        if any(m.group(1) not in PLACEHOLDER_USERS for regex in (MAC_HOME, WIN_HOME) for m in regex.finditer(line)):
            result.append(('personal-home', name, number))
        if any(m.group().lower() != 'tailnet-name.ts.net' and not m.group().lower().endswith('.tailnet-name.ts.net') for m in TAILNET.finditer(line)):
            result.append(('private-tailnet-name', name, number))
        for match in TAIL_IP.finditer(line):
            try:
                address = ipaddress.ip_address(match.group())
            except ValueError:
                continue
            if str(address) not in {'100.64.0.1', '100.64.0.2', '100.64.0.3'}:
                result.append(('private-tailnet-address', name, number))
        if '/examples/' in name and path.suffix.lower() in {'.json', '.md', '.txt'} and any(not m.group().startswith('00000000-0000-0000-0000-') for m in UUID.finditer(line)):
            result.append(('example-session-id', name, number))
    return result


def git(*args, root=ROOT):
    return subprocess.check_output(['git', *args], cwd=root)


def current_files(root=ROOT):
    result = {}
    for raw in git('ls-files', '-z', root=root).split(b'\0'):
        if not raw:
            continue
        name = raw.decode()
        path = root / name
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError(f'Unreviewed link: {name}')
        if path.is_file():
            result[name] = path.read_bytes()
    return result


def inventory_findings(files):
    result = []
    if 'bank/files.json' not in files:
        return result  # Old history may predate the bank.
    inventory = json.loads(files['bank/files.json'])
    expected_names = set(files) - {'bank/files.json'}
    if set(inventory) != expected_names:
        result.append(('inventory-file-set', 'bank/files.json', 0))
    for name, digest in inventory.items():
        if not isinstance(digest, str) or not re.fullmatch('[a-f0-9]{64}', digest):
            result.append(('inventory-invalid-hash', 'bank/files.json', 0))
        elif name not in files or hashlib.sha256(files[name]).hexdigest() != digest:
            result.append(('inventory-byte-mismatch', name, 0))
    return result


def history_findings(root=ROOT):
    result, checked = [], set()
    revisions = git('rev-list', '--all', root=root).decode().splitlines()
    for revision in revisions:
        files = {}
        for entry in git('ls-tree', '-rz', revision, root=root).split(b'\0'):
            if not entry:
                continue
            meta, raw_name = entry.split(b'\t', 1)
            mode, kind, oid = meta.split()
            name = raw_name.decode()
            if kind != b'blob' or mode == b'120000':
                result.append((revision[:12], 'unreviewed-link', name, 0))
                continue
            data = git('cat-file', 'blob', oid.decode(), root=root)
            files[name] = data
            key = (name, oid)
            if key not in checked:
                result.extend((revision[:12], *item) for item in findings(name, data))
                checked.add(key)
        result.extend((revision[:12], *item) for item in inventory_findings(files))
    return result, len(revisions)


def scan_secrets(files, history, root=ROOT):
    if not shutil.which('gitleaks'):
        raise ValueError('Install Gitleaks before --secrets (see docs/public-release.md).')
    config = root / '.gitleaks.toml'
    common = ['--redact', '--no-banner', '--config', str(config)]
    with tempfile.TemporaryDirectory(prefix='fleet-public-scan-') as temp:
        snapshot = Path(temp)
        for name, data in files.items():
            dest = snapshot / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
        subprocess.run(['gitleaks', 'dir', *common, str(snapshot)], check=True, cwd=root)
    if history:
        subprocess.run(['gitleaks', 'git', *common, '--log-opts=--all', '.'], check=True, cwd=root)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--history', action='store_true', help='Check every reachable Git revision.')
    parser.add_argument('--secrets', action='store_true', help='Also require a redacted Gitleaks scan.')
    args = parser.parse_args()
    try:
        files = current_files()
        results = [('working-tree', *item) for name, data in files.items() for item in findings(name, data)]
        results.extend(('working-tree', *item) for item in inventory_findings(files))
        revisions = 0
        if args.history:
            historical, revisions = history_findings()
            results.extend(historical)
        if args.secrets:
            scan_secrets(files, args.history)
        for ref, rule, name, line in results:
            print(f'{ref}: {rule}: {name}:{line}', file=sys.stderr)
        if results:
            print(f'Public check failed: {len(results)} location(s). Values withheld.', file=sys.stderr)
            return 1
        print(f'Public check passed: {len(files)} tracked files; {revisions} historical revision(s).')
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f'Public check failed: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
