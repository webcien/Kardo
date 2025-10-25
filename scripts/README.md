# Publication Scripts

Automated scripts for publishing KardoCore to PyPI.

---

## Scripts

### `publish.py`

Python script that automates the entire PyPI publication process.

**Features:**
- ✅ Prerequisites checking
- ✅ Version validation
- ✅ CHANGELOG verification
- ✅ Build artifacts cleaning
- ✅ Package building (wheel + sdist)
- ✅ Package validation with twine
- ✅ Upload to TestPyPI or PyPI
- ✅ Git tag creation
- ✅ Post-publication verification

### `publish.sh`

Bash wrapper for `publish.py` with Python version checking.

---

## Usage

### Check Package (No Upload)

Validate the package without uploading:

```bash
# Using Python script
python3 scripts/publish.py --check

# Using bash wrapper
./scripts/publish.sh --check
```

**What it does:**
1. Checks prerequisites
2. Validates version
3. Cleans build artifacts
4. Builds package
5. Runs twine check
6. **Does NOT upload**

---

### Publish to TestPyPI

Test the publication process on TestPyPI:

```bash
# Using Python script
python3 scripts/publish.py --test

# Using bash wrapper
./scripts/publish.sh --test
```

**What it does:**
1. All checks from `--check`
2. Uploads to https://test.pypi.org
3. **Does NOT create git tag**

**After upload, test installation:**

```bash
pip install --index-url https://test.pypi.org/simple/ kardocore
kardo --version
```

---

### Publish to Production PyPI

Publish to the real PyPI:

```bash
# Using Python script
python3 scripts/publish.py --prod

# Using bash wrapper
./scripts/publish.sh --prod
```

**What it does:**
1. All checks from `--check`
2. Asks for confirmation (requires typing "yes")
3. Uploads to https://pypi.org
4. Creates and pushes git tag (vX.Y.Z)

**⚠️ Warning:** This cannot be undone. The version cannot be re-uploaded.

---

## Prerequisites

### 1. Install Build Tools

```bash
pip install build twine
```

### 2. Configure PyPI Credentials

Create `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-YOUR-PRODUCTION-TOKEN

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR-TEST-TOKEN
```

**Security:**

```bash
chmod 600 ~/.pypirc
```

### 3. Get API Tokens

**For TestPyPI:**
1. Go to https://test.pypi.org/account/register/
2. Create account and verify email
3. Go to https://test.pypi.org/manage/account/
4. Create API token

**For PyPI:**
1. Go to https://pypi.org/account/register/
2. Create account and verify email
3. Enable 2FA (recommended)
4. Go to https://pypi.org/manage/account/
5. Create API token

---

## Workflow

### Development Workflow

1. **Make changes** to code
2. **Update version** in `setup.py` and `pyproject.toml`
3. **Update CHANGELOG.md** with changes
4. **Commit changes**
5. **Check package**: `./scripts/publish.sh --check`
6. **Test on TestPyPI**: `./scripts/publish.sh --test`
7. **Test installation** from TestPyPI
8. **Publish to PyPI**: `./scripts/publish.sh --prod`

### Quick Release

```bash
# 1. Update version and changelog
vim setup.py pyproject.toml CHANGELOG.md

# 2. Commit
git add .
git commit -m "chore: bump version to 0.2.1"

# 3. Check
./scripts/publish.sh --check

# 4. Publish
./scripts/publish.sh --prod
```

---

## Script Output

### Successful Run

```
======================================================================
                    KardoCore PyPI Publication                        
======================================================================

ℹ️  Mode: Production PyPI

======================================================================
                      Checking Prerequisites                          
======================================================================

✅ Python 3.11.0
✅ Git repository
✅ All required files present
✅ build package installed
✅ twine package installed
✅ No uncommitted changes

======================================================================
                       Version Information                            
======================================================================

ℹ️  Current version: 0.2.0

======================================================================
                       Checking CHANGELOG                             
======================================================================

✅ Version 0.2.0 found in CHANGELOG.md

======================================================================
                    Cleaning Build Artifacts                          
======================================================================

ℹ️  Removed directory: build
ℹ️  Removed directory: dist
✅ Build artifacts cleaned

======================================================================
                        Building Package                              
======================================================================

ℹ️  Building wheel and source distribution...
✅ Generated 2 distribution file(s):
  - kardocore-0.2.0-py3-none-any.whl (8.0 KB)
  - kardocore-0.2.0.tar.gz (72.0 KB)

======================================================================
                       Checking Package                               
======================================================================

ℹ️  Running twine check...
✅ Package passed twine checks

======================================================================
                       Uploading Package                              
======================================================================

⚠️  Uploading to PRODUCTION PyPI...
Are you sure? This cannot be undone. (yes/N): yes
✅ Package uploaded successfully!
ℹ️  View at: https://pypi.org/project/kardocore/0.2.0/

======================================================================
                       Creating Git Tag                               
======================================================================

Create and push tag v0.2.0? (y/N): y
✅ Created tag v0.2.0
✅ Pushed tag v0.2.0 to origin

======================================================================
                         Verification                                 
======================================================================

ℹ️  To test installation from PyPI:
  pip install kardocore
ℹ️  To verify:
  kardo --version
  python -c 'import kardocore; print(kardocore.__version__)'

======================================================================
                      Publication Complete!                           
======================================================================

✅ All steps completed successfully
ℹ️  Next steps:
  1. Verify installation
  2. Update README.md with PyPI badge
  3. Create GitHub release
  4. Announce on social media
```

---

## Error Handling

### Common Errors

#### 1. "build package not installed"

```bash
pip install build
```

#### 2. "twine package not installed"

```bash
pip install twine
```

#### 3. "~/.pypirc not found"

Create the file with your PyPI credentials. See `.pypirc.template`.

#### 4. "Invalid credentials"

Check that your API token in `~/.pypirc` is correct and has not expired.

#### 5. "Package already exists"

You cannot re-upload the same version. Increment the version number.

#### 6. "Uncommitted changes detected"

Commit or stash your changes before publishing.

---

## Advanced Usage

### Dry Run (Check Only)

Always run with `--check` first:

```bash
./scripts/publish.sh --check
```

### Test Before Production

Always test on TestPyPI first:

```bash
# 1. Upload to TestPyPI
./scripts/publish.sh --test

# 2. Test installation
pip install --index-url https://test.pypi.org/simple/ kardocore

# 3. Verify
kardo --version

# 4. If OK, publish to production
./scripts/publish.sh --prod
```

### Skip Git Tag

The script will ask before creating a git tag. Just answer "N" when prompted.

### Manual Upload

If the script fails during upload, you can upload manually:

```bash
# Build first
python3 setup.py sdist bdist_wheel

# Upload
twine upload dist/*
```

---

## Troubleshooting

### Script Fails at Build

```bash
# Clean and try again
rm -rf build/ dist/ *.egg-info/
python3 setup.py sdist bdist_wheel
```

### Upload Fails

```bash
# Check credentials
cat ~/.pypirc

# Test with twine directly
twine upload --repository testpypi dist/*
```

### Version Already Exists

You must increment the version:

1. Edit `setup.py` - change `version="X.Y.Z"`
2. Edit `pyproject.toml` - change `version = "X.Y.Z"`
3. Update `CHANGELOG.md`
4. Commit and run script again

---

## Security Best Practices

1. **Never commit `.pypirc`** - Add to `.gitignore`
2. **Use API tokens** - Never use passwords
3. **Enable 2FA** on PyPI account
4. **Limit token scope** - Use project-specific tokens when possible
5. **Rotate tokens** regularly
6. **Use environment variables** in CI/CD instead of files

---

## CI/CD Integration

For automated publishing with GitHub Actions, see:
- `docs/PYPI_PUBLICATION.md` - Complete guide
- `.github/workflows/publish.yml` - Workflow example

---

## See Also

- `docs/PYPI_PUBLICATION.md` - Detailed publication guide
- `.pypirc.template` - PyPI configuration template
- `CHANGELOG.md` - Version history
- `setup.py` - Package configuration
- `pyproject.toml` - Modern packaging metadata

---

## Support

If you encounter issues:

1. Check `docs/PYPI_PUBLICATION.md` for detailed troubleshooting
2. Review PyPI documentation: https://packaging.python.org/
3. Check twine docs: https://twine.readthedocs.io/
4. Open issue: https://github.com/webcien/Kardo/issues

