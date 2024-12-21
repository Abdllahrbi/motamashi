from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>اختبار</title>
        </head>
        <body dir="rtl">
            <h1>مرحباً بك!</h1>
            <p>هذا اختبار بسيط</p>
        </body>
    </html>
    """

@app.get("/api/test")
async def test():
    return {"message": "تجربة ناجحة!"}
