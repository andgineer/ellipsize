# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python utility library called `ellipsize` that provides pretty-printing and reduction of large Python objects for better visualization. The project uses modern Python packaging with UV as the package manager and follows strict code quality standards.

## Essential Development Commands

### Setup
```bash
# Initial setup - must be run first
source ./activate.sh

# Install/upgrade UV package manager
source ./activate.sh && make uv

# Upgrade all requirements including pre-commit hooks
source ./activate.sh && make reqs
```

**IMPORTANT**: Always activate the virtual environment before running any commands. Use `source ./activate.sh` before each command.

### Testing and Code Quality
```bash
# Run all tests
source ./activate.sh && pytest

# Run pre-commit hooks for code quality
source ./activate.sh && pre-commit run --all-files
```

**IMPORTANT**: Always use `pre-commit run --all-files` for code quality checks. Never run ruff or mypy directly.

Code quality is enforced through pre-commit hooks that run:
- **Ruff**: Linting and formatting (line length: 100 chars for main code, 99 for tests)
- **MyPy**: Static type checking with strict configuration
- **PyTest**: Testing with doctest integration

Coverage thresholds: 85% green, 70% orange

### Documentation
```bash
# Build and serve docs locally (supports: bg, de, en, es, fr, ru)
source ./activate.sh && make docs [language]
```

### Version Management
```bash
source ./activate.sh && make version        # Show current version
source ./activate.sh && make ver-bug        # Bump patch version
source ./activate.sh && make ver-feature    # Bump minor version
source ./activate.sh && make ver-release    # Bump major version
```

## Code Architecture

### Core Structure
- `src/ellipsize/ellipsize.py` - Main ellipsization logic with configurable `max_items_to_show` and `max_item_length` parameters
- `src/ellipsize/__about__.py` - Version information
- `tests/test_ellipsize.py` - Comprehensive test suite

### Key Functionality
The library truncates large Python objects (lists, dicts, nested structures) using ".." to indicate truncated content. It recursively processes nested data structures with configurable limits.

## Development Requirements

- **Python 3.8+** (recommended 3.12)
- **UV package manager** (automatically installed via activate.sh)
- **Source activation script** must be run: `. ./activate.sh`
- Pre-commit hooks are automatically installed for code quality enforcement

## Configuration Details

- Uses modern Python packaging (pyproject.toml with Hatchling build system)
- Dependencies managed through UV with compiled requirements files (`.in` files)
- Documentation built with MkDocs Material with multi-language support
- CI/CD via GitHub Actions with matrix testing across Python versions and operating systems
- Coverage reporting via Codecov and Coveralls
