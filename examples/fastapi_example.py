"""
FastAPI integration example for memhunt

This module demonstrates how to integrate the memory debugging tools
with FastAPI applications.
"""
import logging
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

# Import our memory debugging tools
from pympler import muppy, summary
import objgraph

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Memory Hunt - FastAPI Edition",
              description="Memory debugging tools for FastAPI applications",
              version="0.2.0")

# Set up templates (you would need to create the template files)
templates = Jinja2Templates(directory="templates")


class MemoryDebugger:
    """Memory debugging utilities adapted for FastAPI"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Get a summary of current memory usage"""
        try:
            all_objects = muppy.get_objects()
            mem_summary = summary.summarize(all_objects)
            
            return {
                "total_objects": len(all_objects),
                "summary": [
                    {
                        "type": item[0],
                        "count": item[1],
                        "total_size": item[2]
                    }
                    for item in mem_summary[:20]  # Top 20 types
                ],
                "status": "success"
            }
        except Exception as e:
            self.logger.error(f"Error getting memory summary: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_most_common_types(self) -> Dict[str, Any]:
        """Get most common object types using objgraph"""
        try:
            common_types = objgraph.most_common_types(limit=20)
            return {
                "common_types": [
                    {"type": name, "count": count}
                    for name, count in common_types
                ],
                "status": "success"
            }
        except Exception as e:
            self.logger.error(f"Error getting common types: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_biggest_offender(self) -> Dict[str, Any]:
        """Find the type using the most memory"""
        try:
            all_objects = muppy.get_objects()
            mem_summary = summary.summarize(all_objects)
            
            if mem_summary:
                biggest = max(mem_summary, key=lambda x: x[2])
                return {
                    "biggest_offender": {
                        "type": biggest[0],
                        "count": biggest[1],
                        "total_size": biggest[2]
                    },
                    "status": "success"
                }
            else:
                return {"status": "success", "message": "No memory data available"}
                
        except Exception as e:
            self.logger.error(f"Error getting biggest offender: {e}")
            return {"status": "error", "message": str(e)}


# Initialize the memory debugger
memory_debugger = MemoryDebugger()


@app.get("/")
async def root():
    """Root endpoint with basic info"""
    return {
        "message": "Welcome to Memory Hunt FastAPI Edition",
        "version": "0.2.0",
        "endpoints": {
            "/memory/summary": "Get memory usage summary",
            "/memory/common-types": "Get most common object types",
            "/memory/biggest-offender": "Find biggest memory consumer",
            "/memory/debug": "Full debug information",
            "/docs": "API documentation"
        }
    }


@app.get("/memory/summary")
async def get_memory_summary():
    """Get current memory usage summary"""
    return memory_debugger.get_memory_summary()


@app.get("/memory/common-types")
async def get_common_types():
    """Get most common object types"""
    return memory_debugger.get_most_common_types()


@app.get("/memory/biggest-offender")
async def get_biggest_offender():
    """Get the type consuming the most memory"""
    return memory_debugger.get_biggest_offender()


@app.get("/memory/debug")
async def get_full_debug():
    """Get comprehensive memory debugging information"""
    summary_data = memory_debugger.get_memory_summary()
    common_types = memory_debugger.get_most_common_types()
    biggest_offender = memory_debugger.get_biggest_offender()
    
    return {
        "memory_summary": summary_data,
        "common_types": common_types,
        "biggest_offender": biggest_offender,
        "timestamp": "2024-01-01T00:00:00Z"  # You'd use real timestamp
    }


@app.get("/memory/health")
async def memory_health_check():
    """Basic health check for memory monitoring"""
    try:
        # Quick memory check
        objects = muppy.get_objects()
        return {
            "status": "healthy",
            "total_objects": len(objects),
            "message": "Memory monitoring is operational"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Memory monitoring failed")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception in {request.url}: {exc}")
    return {
        "status": "error",
        "message": "An internal error occurred",
        "detail": str(exc) if app.debug else "Contact administrator"
    }


if __name__ == "__main__":
    # Run the FastAPI application
    uvicorn.run(
        "fastapi_example:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
    
    print("\n" + "="*50)
    print("Memory Hunt FastAPI Server Started!")
    print("\nAvailable endpoints:")
    print("  • http://localhost:8000/ - API overview")
    print("  • http://localhost:8000/memory/summary - Memory usage summary")
    print("  • http://localhost:8000/memory/common-types - Most common types")
    print("  • http://localhost:8000/memory/biggest-offender - Biggest memory user")
    print("  • http://localhost:8000/memory/debug - Full debug info")
    print("  • http://localhost:8000/docs - Interactive API docs")
    print("="*50)
