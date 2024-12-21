from fastapi import FastAPI, Request, HTTPException
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
    BASE_DIR = pathlib.Path("/opt/render/project/src")
else:
    BASE_DIR = pathlib.Path(__file__).parent.parent

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

# قائمة المهام (مؤقتاً في الذاكرة)
tasks = [
    {"id": 1, "title": "إنشاء قاعدة البيانات", "status": "completed"},
    {"id": 2, "title": "تصميم واجهة المستخدم", "status": "in_progress"},
    {"id": 3, "title": "كتابة الوثائق", "status": "pending"}
]

# الصفحة الرئيسية
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    try:
        print("Attempting to render home.html")
        return templates.TemplateResponse(
            "home.html",
            {
                "request": request,
                "title": "متماشي - نظام إدارة المهام",
                "tasks": tasks
            }
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# صفحة المهام
@app.get("/tasks", response_class=HTMLResponse)
async def tasks(request: Request):
    try:
        return templates.TemplateResponse(
            "tasks.html",
            {
                "request": request,
                "title": "المهام",
                "tasks": tasks
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
    return {"tasks": tasks}

@app.post("/api/tasks")
async def create_task(task: dict):
    task_id = max([t["id"] for t in tasks]) + 1
    new_task = {
        "id": task_id,
        "title": task["title"],
        "status": "pending"
    }
    tasks.append(new_task)
    return {"success": True, "task": new_task}

@app.put("/api/tasks/{task_id}")
async def update_task(task_id: int, task_update: dict):
    for task in tasks:
        if task["id"] == task_id:
            if "status" in task_update:
                task["status"] = task_update["status"]
            if "title" in task_update:
                task["title"] = task_update["title"]
            return {"success": True, "task": task}
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return {"success": True}
    raise HTTPException(status_code=404, detail="Task not found")
