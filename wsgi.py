from app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("wsgi:app", host="127.0.0.1", port=3000, reload=True)
