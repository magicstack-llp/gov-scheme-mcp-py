# Publishing Guide

This guide explains how to publish the `gov-scheme-mcp` package to PyPI.

## Prerequisites

1. Install build and publishing tools:

    ```bash
    pip install build twine
    ```

2. Create accounts on PyPI:

    - Test PyPI: https://test.pypi.org/account/register/
    - Production PyPI: https://pypi.org/account/register/

3. Create API tokens:
    - Generate tokens in your PyPI account settings
    - Store them securely

## Building the Package

1. Clean previous builds:

    ```bash
    rm -rf dist/ build/ src/*.egg-info/
    ```

2. Build the package:

    ```bash
    python -m build
    ```

    This creates:

    - `dist/gov_scheme_mcp-X.Y.Z.tar.gz` (source distribution)
    - `dist/gov_scheme_mcp-X.Y.Z-py3-none-any.whl` (wheel distribution)

## Publishing to Test PyPI

Test your package first:

```bash
python -m twine upload --repository testpypi dist/*
```

Test installation:

```bash
pip install --index-url https://test.pypi.org/simple/ gov-scheme-mcp
```

## Publishing to Production PyPI

When ready for production:

```bash
python -m twine upload dist/*
```

## Version Management

Update version in `pyproject.toml`:

```toml
[project]
version = "0.2.0"  # Update this
```

Also update in `src/gov_scheme_mcp/__init__.py`:

```python
__version__ = "0.2.0"  # Update this
```

## Configuration Files

### .pypirc

Create `~/.pypirc` for authentication:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = <your-pypi-token>

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = <your-test-pypi-token>
```

## Automated Publishing with GitHub Actions

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
            - uses: actions/checkout@v4
            - name: Set up Python
              uses: actions/setup-python@v4
              with:
                  python-version: "3.10"
            - name: Install dependencies
              run: |
                  python -m pip install --upgrade pip
                  pip install build twine
            - name: Build package
              run: python -m build
            - name: Publish to PyPI
              env:
                  TWINE_USERNAME: __token__
                  TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
              run: twine upload dist/*
```

Store your PyPI API token in GitHub repository secrets as `PYPI_API_TOKEN`.

## Checklist Before Publishing

-   [ ] Update version numbers
-   [ ] Update CHANGELOG.md (if you have one)
-   [ ] Run tests: `pytest`
-   [ ] Check package builds: `python -m build`
-   [ ] Test installation locally: `pip install -e .`
-   [ ] Update README.md if needed
-   [ ] Commit and tag the release
-   [ ] Test on Test PyPI first
-   [ ] Publish to production PyPI

## Post-Publication

1. Verify installation:

    ```bash
    pip install gov-scheme-mcp
    ```

2. Test the CLI:

    ```bash
    gov-scheme-mcp
    ```

3. Update documentation and GitHub repository with installation instructions.
