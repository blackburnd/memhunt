========
memhunt
========

memhunt is a modern Python memory debugging and profiling toolkit, originally based on z3c.memhunt.objgraph.
This package has been completely modernized to work with Python 3.8+ and is now framework-agnostic.

memhunt uses objgraph and pympler to help locate and diagnose memory leaks in Python applications.
It provides both web-based interfaces (using Jinja2 templates) and programmatic APIs for memory analysis.

Features
--------

* Memory usage analysis and reporting
* Object reference counting and visualization  
* Memory leak detection
* Reference graph generation (requires graphviz)
* Framework-agnostic (works with any Python application)
* FastAPI integration example
* Modern Jinja2 templates for web interfaces
* Comprehensive test suite

Installation
------------

Install memhunt using pip:

    pip install memhunt

For FastAPI integration:

    pip install memhunt[fastapi]

For development:

    pip install memhunt[dev]

Quick Start
-----------

Basic memory analysis:

    from memhunt.browser.views import DebugView
    
    debug = DebugView()
    print(debug.memory())  # Print memory summary
    print(debug.get_biggest_offender())  # Find biggest memory consumer

Web interface example with FastAPI:

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

Requirements
------------

* Python 3.8+
* pympler>=0.9
* objgraph>=3.5.0  
* jinja2>=3.0.0

For graphical output (optional):
* graphviz

Testing
-------

Run tests:

    pytest tests/

With coverage:

    pytest tests/ --cov=memhunt --cov-report=term-missing

License
-------

This package is licensed under the Zope Public License (ZPL) 2.1.
