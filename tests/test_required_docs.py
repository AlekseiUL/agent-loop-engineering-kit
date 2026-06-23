from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_required_files_exist():
    required=['README.md','START-HERE.md','docs/00-what-is-agent-loop-engineering.md','schemas/loop-spec.schema.json','templates/loop-spec.yaml','tests/test_loop_spec_schema.py']
    assert not [p for p in required if not (ROOT/p).exists()]
def test_readme_does_not_overclaim():
    text=(ROOT/'README.md').read_text(encoding='utf-8').lower()
    for banned in ['fully autonomous','safe autopilot','no human review needed']:
        assert banned not in text
    assert 'not a replacement for hermes' in text
