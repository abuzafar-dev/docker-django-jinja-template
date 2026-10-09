import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import jinja2
from django.test import SimpleTestCase, override_settings


class JinjaTemplateTests(SimpleTestCase):
    def test_patched_jinja_version(self):
        self.assertGreaterEqual(tuple(int(x) for x in jinja2.__version__.split('.')[:3]), (3, 1, 6))

    @override_settings(ALLOWED_HOSTS=['testserver'])
    def test_home_renders_with_jinja(self):
        response = self.client.get('/')
        self.assertContains(response, 'This page is rendered with Jinja.')
        self.assertContains(response, 'href="/"')


class ProductionDefaultsTests(SimpleTestCase):
    def test_debug_off_when_env_missing(self):
        root = Path(__file__).resolve().parent.parent
        copy = Path(tempfile.mkdtemp()) / 'project'
        shutil.copytree(root, copy, ignore=shutil.ignore_patterns('.env', '.git', '*.sqlite3'))
        env = {k: v for k, v in os.environ.items() if k not in ('DEBUG', 'POSTGRES_DB')}
        env.update(SECRET_KEY='x' * 50, DJANGO_SETTINGS_MODULE='root.settings')
        code = "from django.conf import settings as s; print(s.DEBUG)"
        result = subprocess.run([sys.executable, '-c', code], cwd=copy, env=env, capture_output=True, text=True)
        self.assertEqual(result.stdout.strip(), 'False', result.stderr)
