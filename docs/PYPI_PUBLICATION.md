# PyPI Publication Guide

Complete guide for publishing **KardoCore** to PyPI (Python Package Index).

---

## Prerequisites

### 1. Install Build Tools

```bash
pip install --upgrade build twine
```

### 2. Create PyPI Account

1. Go to https://pypi.org/account/register/
2. Verify your email
3. Enable 2FA (recommended)

### 3. Create API Token

1. Go to https://pypi.org/manage/account/
2. Scroll to "API tokens"
3. Click "Add API token"
4. Name: `kardocore-upload`
5. Scope: "Entire account" or "Project: kardocore"
6. Copy the token (starts with `pypi-`)

### 4. Configure .pypirc

Create `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-YOUR-TOKEN-HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR-TESTPYPI-TOKEN-HERE
```

**Security**: Set permissions:

```bash
chmod 600 ~/.pypirc
```

---

## Publication Process

### Step 1: Clean Previous Builds

```bash
rm -rf build/ dist/ *.egg-info/
```

### Step 2: Update Version

Update version in:
- `setup.py` - Line 39
- `pyproject.toml` - Line 6
- `kardocore/__init__.py` (if exists)

### Step 3: Update CHANGELOG.md

Add release notes:

```markdown
## [0.2.0] - 2025-01-24

### Added
- Database support (SQLite, PostgreSQL)
- Authentication & Security module
- CLI implementation (kardo command)
- Migration system
- Example applications
- Integration tests

### Changed
- Improved documentation
- Updated dependencies

### Fixed
- Python 3.11 compatibility
```

### Step 4: Build Distribution

```bash
python3 -m build
```

This creates:
- `dist/kardocore-0.2.0-py3-none-any.whl` (wheel)
- `dist/kardocore-0.2.0.tar.gz` (source distribution)

### Step 5: Check Distribution

```bash
twine check dist/*
```

Expected output:

```
Checking dist/kardocore-0.2.0-py3-none-any.whl: PASSED
Checking dist/kardocore-0.2.0.tar.gz: PASSED
```

### Step 6: Test on TestPyPI (Optional but Recommended)

Upload to TestPyPI first:

```bash
twine upload --repository testpypi dist/*
```

Test installation:

```bash
pip install --index-url https://test.pypi.org/simple/ kardocore
```

### Step 7: Upload to PyPI

```bash
twine upload dist/*
```

Expected output:

```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading kardocore-0.2.0-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 50.0/50.0 kB • 00:00 • ?
Uploading kardocore-0.2.0.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 45.0/45.0 kB • 00:00 • ?

View at:
https://pypi.org/project/kardocore/0.2.0/
```

### Step 8: Verify Installation

```bash
pip install kardocore
```

Test the installation:

```bash
kardo --version
# Output: KardoCore v0.2.0

python3 -c "import kardocore; print(kardocore.__version__)"
# Output: 0.2.0
```

---

## Automated Publication with GitHub Actions

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Check package
      run: twine check dist/*
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

**Setup:**

1. Go to GitHub repository settings
2. Secrets and variables → Actions
3. New repository secret
4. Name: `PYPI_API_TOKEN`
5. Value: Your PyPI token

**Usage:**

1. Create a new release on GitHub
2. GitHub Actions automatically publishes to PyPI

---

## Version Management

### Semantic Versioning

KardoCore follows [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 0.2.0)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Version Branches

- `main` - Development (v0.1.0-alpha, Python 3.14+)
- `v0.0.9` - Stable (v0.0.9, Python 3.11+)

### Release Process

1. **Development** → `main` branch
2. **Testing** → Create release candidate (e.g., 0.2.0-rc1)
3. **Stable** → Tag and release (e.g., 0.2.0)
4. **Backport** → Merge to stable branch if needed

---

## Troubleshooting

### Error: "Package already exists"

You cannot re-upload the same version. Options:

1. Increment version (recommended)
2. Delete from PyPI (not recommended)

### Error: "Invalid credentials"

Check:

1. Token is correct in `~/.pypirc`
2. Token has not expired
3. Token has correct scope

### Error: "File already exists"

Clean build artifacts:

```bash
rm -rf build/ dist/ *.egg-info/
python3 -m build
```

### Error: "Long description has syntax errors"

Check README.md:

```bash
python3 -m readme_renderer README.md
```

### Warning: "Unknown distribution option"

Update setuptools:

```bash
pip install --upgrade setuptools
```

---

## Best Practices

### 1. **Test Before Publishing**

Always test on TestPyPI first:

```bash
twine upload --repository testpypi dist/*
```

### 2. **Use API Tokens**

Never use passwords. Always use API tokens.

### 3. **Verify Package**

After publishing, install and test:

```bash
pip install kardocore
kardo --version
```

### 4. **Update Documentation**

Update README.md with installation instructions:

```markdown
## Installation

```bash
pip install kardocore
```
```

### 5. **Tag Releases**

Create Git tags for releases:

```bash
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin v0.2.0
```

### 6. **Changelog**

Maintain CHANGELOG.md with all changes.

### 7. **Security**

- Never commit `.pypirc`
- Use environment variables in CI/CD
- Enable 2FA on PyPI

---

## Post-Publication

### 1. Announce Release

- GitHub Releases
- Twitter/Social media
- Reddit (r/Python)
- Python Weekly
- Discord/Slack communities

### 2. Update Documentation

- Update README.md
- Update installation guides
- Update version badges

### 3. Monitor

- PyPI downloads: https://pypistats.org/packages/kardocore
- GitHub stars and issues
- User feedback

---

## Package Information

### PyPI URLs

- **Package**: https://pypi.org/project/kardocore/
- **Stats**: https://pypistats.org/packages/kardocore
- **JSON API**: https://pypi.org/pypi/kardocore/json

### Installation

```bash
# Latest version
pip install kardocore

# Specific version
pip install kardocore==0.2.0

# With extras
pip install kardocore[postgresql]
pip install kardocore[all]

# Development version
pip install git+https://github.com/webcien/Kardo.git@main
```

### Uninstallation

```bash
pip uninstall kardocore
```

---

## Quick Reference

### Build

```bash
python3 -m build
```

### Check

```bash
twine check dist/*
```

### Upload to TestPyPI

```bash
twine upload --repository testpypi dist/*
```

### Upload to PyPI

```bash
twine upload dist/*
```

### Clean

```bash
rm -rf build/ dist/ *.egg-info/
```

---

## See Also

- [PyPI Documentation](https://packaging.python.org/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [Setuptools Documentation](https://setuptools.pypa.io/)
- [PEP 517](https://peps.python.org/pep-0517/) - Build system
- [PEP 518](https://peps.python.org/pep-0518/) - pyproject.toml

---

## Support

- **GitHub**: https://github.com/webcien/Kardo
- **Issues**: https://github.com/webcien/Kardo/issues
- **Discussions**: https://github.com/webcien/Kardo/discussions

