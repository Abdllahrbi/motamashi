import uvicorn
from pathlib import Path

if __name__ == "__main__":
    # Get the absolute path to the project directory
    project_dir = Path(__file__).resolve().parent
    
    # Add the project directory to Python path
    import sys
    sys.path.append(str(project_dir))
    
    # Run the application
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=[str(project_dir)]
    )
