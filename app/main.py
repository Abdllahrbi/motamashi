from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import traceback
import os
import pathlib

app = FastAPI()

# الحصول على المسار المطلق للملفات
import pathlib
import os

if os.environ.get('RENDER'):
    BASE_DIR = pathlib.Path("/opt/render/project/src/app")
else:
    BASE_DIR = pathlib.Path(__file__).parent

TEMPLATES_DIR = str(BASE_DIR / "templates")
STATIC_DIR = str(BASE_DIR / "static")

print(f"Base Directory: {BASE_DIR}")
print(f"Templates Directory: {TEMPLATES_DIR}")
print(f"Static Directory: {STATIC_DIR}")

# تكوين القوالب والملفات الثابتة
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.get("/debug")
async def debug_info():
    return {
        "base_dir": BASE_DIR,
        "templates_dir": TEMPLATES_DIR,
        "static_dir": STATIC_DIR,
        "templates_exists": os.path.exists(TEMPLATES_DIR),
        "static_exists": os.path.exists(STATIC_DIR),
        "template_files": os.listdir(TEMPLATES_DIR) if os.path.exists(TEMPLATES_DIR) else [],
        "static_files": os.listdir(STATIC_DIR) if os.path.exists(STATIC_DIR) else []
    }

# الصفحة الرئيسية
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    try:
        print("Attempting to render index.html")
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "title": "متماشي - نظام إدارة المهام",
                "tasks": [
                    {"id": 1, "title": "إنشاء قاعدة البيانات", "status": "completed"},
                    {"id": 2, "title": "تصميم واجهة المستخدم", "status": "in_progress"},
                    {"id": 3, "title": "كتابة الوثائق", "status": "pending"}
                ]
            }
        )
    except Exception as e:
        print(f"Error in home route: {str(e)}")
        print(traceback.format_exc())
        return HTMLResponse(
            content=f"""
            <html dir="rtl" lang="ar">
                <head><title>خطأ</title></head>
                <body>
                    <h1>خطأ في النظام</h1>
                    <p>نوع الخطأ: {str(e)}</p>
                    <pre>{traceback.format_exc()}</pre>
                </body>
            </html>
            """,
            status_code=500
        )

# صفحة المهام
@app.get("/tasks", response_class=HTMLResponse)
async def tasks(request: Request):
    try:
        return templates.TemplateResponse(
            "tasks.html",
            {
                "request": request,
                "title": "المهام",
                "tasks": [
                    {"id": 1, "title": "إنشاء قاعدة البيانات", "status": "completed"},
                    {"id": 2, "title": "تصميم واجهة المستخدم", "status": "in_progress"},
                    {"id": 3, "title": "كتابة الوثائق", "status": "pending"}
                ]
            }
        )
    except Exception as e:
        print(f"Error in tasks route: {str(e)}")
        print(traceback.format_exc())
        return HTMLResponse(
            content=f"<h1>خطأ</h1><p>{str(e)}</p><pre>{traceback.format_exc()}</pre>",
            status_code=500
        )

# واجهة برمجة التطبيقات للمهام
@app.get("/api/tasks")
async def get_tasks():
    try:
        return [
            {"id": 1, "title": "إنشاء قاعدة البيانات", "status": "completed"},
            {"id": 2, "title": "تصميم واجهة المستخدم", "status": "in_progress"},
            {"id": 3, "title": "كتابة الوثائق", "status": "pending"}
        ]
    except Exception as e:
        print(f"Error in API route: {str(e)}")
        print(traceback.format_exc())
        return {"error": str(e), "traceback": traceback.format_exc()}
