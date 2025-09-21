# FastAPI Example for memhunt

This directory contains a FastAPI integration example showing how to use memhunt in modern web applications.

## Usage

1. Install dependencies:
```bash
pip install memhunt[fastapi]
```

2. Run the example:
```bash
python examples/fastapi_example.py
```

3. Visit http://localhost:8000/docs for interactive API documentation

## Available Endpoints

- `/memory/summary` - Get memory usage summary
- `/memory/common-types` - Get most common object types  
- `/memory/biggest-offender` - Find biggest memory consumer
- `/memory/debug` - Full debug information
- `/memory/health` - Health check endpoint
