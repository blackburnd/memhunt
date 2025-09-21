# memhunt - Modernization Complete! ✅

## Overview
Successfully modernized the legacy z3c.memhunt.objgraph package from Python 2/Zope-specific code to a modern Python 3.8+ package called **memhunt**.

## Key Modernizations Completed

### 1. Package Rename & Framework Independence
- ✅ **Renamed from z3c.memhunt.objgraph to memhunt**
- ✅ **Removed ALL Zope dependencies** - package is now framework-agnostic
- ✅ Works with any Python application (Flask, Django, FastAPI, etc.)

### 2. Python 3 Compatibility
- ✅ Updated all code to Python 3.8+ standards
- ✅ Added comprehensive type annotations throughout
- ✅ Replaced legacy `print` statements with modern `f-strings`
- ✅ Updated exception handling to modern Python syntax

### 3. Dependency Modernization
- ✅ **Replaced guppy with pympler** - guppy was unmaintained and Python 2 only
- ✅ **Replaced Zope Page Templates with Jinja2** - modern, lightweight template engine
- ✅ Updated to use modern `objgraph` library for memory debugging

### 4. Template System Overhaul
- ✅ Completely replaced Zope Page Templates (.pt files) with Jinja2 (.html templates)
- ✅ Created modern HTML5 templates with clean CSS styling
- ✅ Templates: `start.html`, `ref_count.html`, `ref_common_count.html`
- ✅ Implemented `BaseView` class with Jinja2 integration

### 5. Testing Infrastructure
- ✅ **Replaced Plone TestCase with pytest** - modern testing framework
- ✅ Created comprehensive test suite with 21 test cases
- ✅ Added pytest-cov for coverage reporting
- ✅ **66% test coverage** on core views module
- ✅ All tests passing ✨

### 6. Modern Packaging
- ✅ Created `pyproject.toml` for modern Python packaging
- ✅ Updated `setup.py` with current best practices
- ✅ Proper dependency specification with version constraints
- ✅ Added development dependencies (pytest, coverage, etc.)

### 7. FastAPI Integration
- ✅ Created modern REST API example using FastAPI
- ✅ Web-based memory debugging endpoints
- ✅ JSON responses for programmatic access
- ✅ Modern async/await patterns

## Test Results

```bash
$ pytest tests/ -v --cov=memhunt --cov-report=term-missing

======================= 21 passed in 5.41s =======================

Coverage Report:
memhunt/browser/views.py     229     78    66%
```

## Installation & Usage

### Install from PyPI (when published)
```bash
pip install memhunt
```

### Development Installation
```bash
git clone https://github.com/blackburnd/memhunt.git
cd memhunt
pip install -e .[dev]
```

### Quick Start
```python
from memhunt.browser.views import DebugView

debug = DebugView()
print(debug.memory())  # Print memory summary
print(debug.get_biggest_offender())  # Find biggest memory consumer
```

### FastAPI Integration
```python
from fastapi import FastAPI
from memhunt.browser.views import Start, DebugView

app = FastAPI()

@app.get("/memhunt/")
def memory_debug():
    view = Start()
    return view()

@app.get("/memhunt/memory")  
def memory_summary():
    debug = DebugView()
    return {"memory": debug.memory()}
```

## Dependencies

### Runtime Dependencies
- **jinja2** - Modern template engine (replaced Zope Page Templates)
- **pympler** - Memory profiling (replaced guppy)  
- **objgraph** - Object reference tracking

### Development Dependencies  
- **pytest** - Modern testing framework
- **pytest-cov** - Coverage reporting
- **pytest-mock** - Mocking utilities

## Benefits of Modernization

1. **Framework Independence** - No longer tied to Zope/Plone
2. **Python 3 Native** - Uses modern Python features and performance
3. **Maintainable Dependencies** - All dependencies are actively maintained
4. **Better Testing** - Comprehensive test suite with good coverage
5. **Modern Deployment** - Can be deployed anywhere (FastAPI, Flask, Django, etc.)
6. **Type Safety** - Full type annotations for better IDE support
7. **Performance** - Modern libraries and Python 3 optimizations

## License

This package is licensed under the Zope Public License (ZPL) 2.1.
