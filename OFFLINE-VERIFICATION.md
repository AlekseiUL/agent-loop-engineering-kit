# Offline verification boundary

A universal pinned CI/release dependency constraints file and read-only workflow permissions.

## Reproduce

`python -m pip install -c requirements-ci.lock ".[dev]"; python -m pytest`

Use the same constraints for release verification. Update with uv pip compile pyproject.toml --extra dev --python-version 3.11 --universal -o requirements-ci.lock, then rerun tests.

## Rollback

Review the commit diff and use a new checkout of the pre-change commit for source rollback. Keep user data and live installations untouched. A source rollback is not permission to restore unsafe network exposure or bypass approval.
