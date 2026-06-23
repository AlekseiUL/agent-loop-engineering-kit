from pathlib import Path
import tomllib
ROOT=Path(__file__).resolve().parents[1]
def test_required_files_exist():
    required=['README.md','START-HERE.md','docs/00-what-is-agent-loop-engineering.md','docs/09-production-readiness.md','schemas/loop-spec.schema.json','templates/loop-spec.yaml','tests/test_loop_spec_schema.py']
    assert not [p for p in required if not (ROOT/p).exists()]


def test_package_version_matches_project_metadata():
    project = tomllib.loads((ROOT/'pyproject.toml').read_text(encoding='utf-8'))['project']
    init_text = (ROOT/'hermes_loop/__init__.py').read_text(encoding='utf-8')
    assert f'__version__ = "{project["version"]}"' in init_text


def test_license_is_complete_mit_text():
    text=(ROOT/'LICENSE').read_text(encoding='utf-8')
    assert text.startswith('MIT License')
    assert 'Permission is hereby granted, free of charge' in text
    assert 'THE SOFTWARE IS PROVIDED "AS IS"' in text
    assert 'LIABILITY, WHETHER IN AN ACTION OF CONTRACT' in text


def test_readme_does_not_overclaim():
    text=(ROOT/'README.md').read_text(encoding='utf-8').lower()
    for banned in ['fully autonomous','safe autopilot','no human review needed']:
        assert banned not in text
    assert 'not a replacement for hermes' in text
