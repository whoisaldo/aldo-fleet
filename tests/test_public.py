import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('check_public', ROOT / 'scripts/check-public.py')
public = importlib.util.module_from_spec(spec)
spec.loader.exec_module(public)


class PublicReleaseTests(unittest.TestCase):
    def test_private_metadata_is_detected_without_echoing_values(self):
        # Fictional fixtures, never real owner metadata.
        private = '/' + 'Users/fixture-person/app\nhttps://' + '.'.join(['node', 'fixture-tailnet', 'ts', 'net']) + '\n' + '.'.join(['100', '100', '1', '2'])
        result = public.findings('example.md', private.encode())
        self.assertEqual({x[0] for x in result}, {'personal-home', 'private-tailnet-name', 'private-tailnet-address'})
        self.assertNotIn('fixture-person', repr(result))

    def test_placeholders_and_example_session_ids_are_allowed(self):
        example = '/Users/your-user/app\nhttps://devbox1.tailnet-name.ts.net\n100.64.0.1'
        self.assertEqual(public.findings('example.md', example.encode()), [])
        self.assertEqual(public.findings('skill/examples/report.json', b'00000000-0000-0000-0000-000000000001'), [])
        self.assertTrue(public.findings('skill/examples/report.json', b'11111111-1111-1111-1111-111111111111'))

    def test_state_files_fail_even_when_empty(self):
        for name in ['auth.json', 'private/cookies.json', 'x/.env', 'x/cache.sqlite', 'x/backups/note.md', 'x/canvas-planning/config.json']:
            self.assertIn('private-state-file', {x[0] for x in public.findings(name, b'')})
        self.assertEqual(public.findings('config.example.json', b'{}'), [])

    def test_inventory_allowance_requires_real_source_hashes(self):
        import hashlib
        import json
        files = {'demo.md': b'example'}
        files['bank/files.json'] = json.dumps({'demo.md': hashlib.sha256(files['demo.md']).hexdigest()}).encode()
        self.assertEqual(public.inventory_findings(files), [])
        files['demo.md'] = b'changed'
        self.assertTrue(public.inventory_findings(files))

    def test_history_detects_data_deleted_from_tip(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            def git(*args):
                return subprocess.run(['git', *args], cwd=root, check=True, capture_output=True)
            git('init', '-q')
            git('config', 'user.name', 'Example')
            git('config', 'user.email', 'example@example.com')
            (root / 'demo.md').write_text('/' + 'Users/fixture-person/project')
            git('add', '.')
            git('commit', '-qm', 'Fictional private fixture')
            (root / 'demo.md').write_text('/Users/your-user/project')
            git('commit', '-qam', 'Replace with example')
            self.assertEqual(public.findings('demo.md', (root / 'demo.md').read_bytes()), [])
            found, count = public.history_findings(root)
            self.assertEqual(count, 2)
            self.assertEqual({x[1] for x in found}, {'personal-home'})
