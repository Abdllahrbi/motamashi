// إضافة مهمة جديدة
document.getElementById('add-task').addEventListener('click', () => {
    const title = prompt('أدخل عنوان المهمة الجديدة:');
    if (title) {
        fetch('/api/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            }
        });
    }
});

// تعديل حالة المهمة
document.querySelectorAll('.edit-task').forEach(button => {
    button.addEventListener('click', () => {
        const taskId = button.dataset.taskId;
        const newStatus = prompt('أدخل الحالة الجديدة (completed, in_progress, pending):');
        if (newStatus) {
            fetch(`/api/tasks/${taskId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ status: newStatus }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.reload();
                }
            });
        }
    });
});

// حذف مهمة
document.querySelectorAll('.delete-task').forEach(button => {
    button.addEventListener('click', () => {
        const taskId = button.dataset.taskId;
        if (confirm('هل أنت متأكد من حذف هذه المهمة؟')) {
            fetch(`/api/tasks/${taskId}`, {
                method: 'DELETE',
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.reload();
                }
            });
        }
    });
});
