from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime

app = FastAPI(title="متماشي")

# إعداد الملفات الثابتة والقوالب
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# المهام للعرض
TASKS = [
    {"id": 1, "title": "إنشاء قاعدة البيانات", "status": "completed"},
    {"id": 2, "title": "تصميم واجهة المستخدم", "status": "in_progress"},
    {"id": 3, "title": "كتابة الوثائق", "status": "pending"}
]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "tasks": TASKS,
            "current_date": datetime.now()
        }
    )

@app.get("/tasks", response_class=HTMLResponse)
async def tasks_page(request: Request):
    return templates.TemplateResponse(
        "tasks.html",
        {
            "request": request,
            "tasks": TASKS
        }
    )

@app.get("/api/tasks")
async def get_tasks():
    return TASKS
