document.addEventListener('DOMContentLoaded', function() {
    initializeCalendar();
    initializeTaskProgress();
    setupEventListeners();

    // Initialize progress circles
    const progressCircles = document.querySelectorAll('.progress-circle');
    progressCircles.forEach(circle => {
        const progress = circle.getAttribute('data-progress');
        updateProgressCircle(circle, progress);
    });

    // Initialize task cards
    const taskCards = document.querySelectorAll('.task-card');
    taskCards.forEach(card => {
        card.addEventListener('click', () => {
            // Remove active class from all cards
            taskCards.forEach(c => c.classList.remove('active'));
            // Add active class to clicked card
            card.classList.add('active');
            // Update task details panel
            updateTaskDetails(card.dataset.taskId);
        });
    });

    // Search functionality
    const searchBox = document.querySelector('.search-box');
    if (searchBox) {
        searchBox.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            filterTasks(searchTerm);
        });
    }
});

function initializeCalendar() {
    const calendarGrid = document.querySelector('.grid-cols-7');
    const daysInMonth = new Date(new Date().getFullYear(), new Date().getMonth() + 1, 0).getDate();
    const firstDay = new Date(new Date().getFullYear(), new Date().getMonth(), 1).getDay();

    // Add empty cells for days before the first day of the month
    for (let i = 0; i < firstDay; i++) {
        const emptyDay = document.createElement('div');
        calendarGrid.appendChild(emptyDay);
    }

    // Add days of the month
    for (let day = 1; day <= daysInMonth; day++) {
        const dayElement = document.createElement('div');
        dayElement.className = 'calendar-day';
        dayElement.textContent = day;
        
        if (day === new Date().getDate()) {
            dayElement.classList.add('active');
        }
        
        dayElement.addEventListener('click', () => selectDate(day));
        calendarGrid.appendChild(dayElement);
    }
}

function initializeTaskProgress() {
    const tasks = document.querySelectorAll('.task-progress');
    tasks.forEach(task => {
        const progress = parseInt(task.dataset.progress);
        const circle = task.querySelector('circle:not(.bg)');
        const radius = circle.r.baseVal.value;
        const circumference = 2 * Math.PI * radius;
        
        circle.style.strokeDasharray = circumference;
        circle.style.strokeDashoffset = circumference - (progress / 100) * circumference;
    });
}

function setupEventListeners() {
    // Add task button
    const addTaskBtn = document.querySelector('.add-task-button');
    if (addTaskBtn) {
        addTaskBtn.addEventListener('click', () => {
            // Show task creation modal
            showTaskModal();
        });
    }

    // Task completion toggles
    const taskCheckboxes = document.querySelectorAll('.task-checkbox');
    taskCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', (e) => {
            const taskId = e.target.dataset.taskId;
            updateTaskStatus(taskId, e.target.checked);
        });
    });
}

function selectDate(day) {
    const allDays = document.querySelectorAll('.calendar-day');
    allDays.forEach(d => d.classList.remove('active'));
    
    const selectedDay = Array.from(allDays).find(d => d.textContent == day);
    if (selectedDay) {
        selectedDay.classList.add('active');
        fetchTasksForDate(day);
    }
}

async function fetchTasksForDate(day) {
    try {
        const response = await fetch(`/api/tasks/${day}`);
        const tasks = await response.json();
        updateDailyTasks(tasks);
    } catch (error) {
        console.error('Error fetching tasks:', error);
    }
}

function updateDailyTasks(tasks) {
    const tasksContainer = document.getElementById('daily-tasks');
    tasksContainer.innerHTML = '';

    tasks.forEach(task => {
        const taskElement = createTaskElement(task);
        tasksContainer.appendChild(taskElement);
    });
}

function createTaskElement(task) {
    const div = document.createElement('div');
    div.className = 'task-card';
    div.innerHTML = `
        <div class="flex justify-between items-center">
            <div>
                <h3 class="font-semibold">${task.title}</h3>
                <p class="text-sm text-gray-400">${task.time}</p>
            </div>
            <div class="task-progress" data-progress="${task.progress}">
                <svg width="60" height="60">
                    <circle class="bg" cx="30" cy="30" r="26" />
                    <circle cx="30" cy="30" r="26" />
                </svg>
                <span class="absolute inset-0 flex items-center justify-center">
                    ${task.progress}%
                </span>
            </div>
        </div>
    `;
    return div;
}

function showTaskModal() {
    // Implement task creation modal logic
    console.log('Show task creation modal');
}

async function updateTaskStatus(taskId, completed) {
    try {
        const response = await fetch(`/api/tasks/${taskId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ completed })
        });
        
        if (response.ok) {
            updateTaskProgress();
        }
    } catch (error) {
        console.error('Error updating task:', error);
    }
}

function updateTaskProgress() {
    // Update overall progress bar and task counts
    const progressBar = document.querySelector('.progress-bar');
    const tasksCompleted = document.querySelectorAll('.task-checkbox:checked').length;
    const totalTasks = document.querySelectorAll('.task-checkbox').length;
    
    const percentage = (tasksCompleted / totalTasks) * 100;
    progressBar.style.width = `${percentage}%`;
    
    document.querySelector('.tasks-count').textContent = `${tasksCompleted}/${totalTasks}`;
}

function updateProgressCircle(circle, progress) {
    // Create SVG circle with progress
    const radius = 18;
    const circumference = 2 * Math.PI * radius;
    const dashOffset = circumference * (1 - progress / 100);
    
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', '40');
    svg.setAttribute('height', '40');
    svg.setAttribute('viewBox', '0 0 40 40');
    
    const circleEl = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circleEl.setAttribute('cx', '20');
    circleEl.setAttribute('cy', '20');
    circleEl.setAttribute('r', radius);
    circleEl.setAttribute('fill', 'none');
    circleEl.setAttribute('stroke', 'rgba(255, 255, 255, 0.1)');
    circleEl.setAttribute('stroke-width', '4');
    
    const progressCircleEl = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    progressCircleEl.setAttribute('cx', '20');
    progressCircleEl.setAttribute('cy', '20');
    progressCircleEl.setAttribute('r', radius);
    progressCircleEl.setAttribute('fill', 'none');
    progressCircleEl.setAttribute('stroke', 'white');
    progressCircleEl.setAttribute('stroke-width', '4');
    progressCircleEl.setAttribute('stroke-dasharray', circumference);
    progressCircleEl.setAttribute('stroke-dashoffset', dashOffset);
    progressCircleEl.setAttribute('transform', 'rotate(-90 20 20)');
    
    svg.appendChild(circleEl);
    svg.appendChild(progressCircleEl);
    
    // Add progress text
    const text = document.createElement('span');
    text.textContent = progress + '%';
    text.style.position = 'absolute';
    text.style.top = '50%';
    text.style.left = '50%';
    text.style.transform = 'translate(-50%, -50%)';
    text.style.fontSize = '12px';
    text.style.color = 'white';
    
    circle.innerHTML = '';
    circle.appendChild(svg);
    circle.appendChild(text);
}

function filterTasks(searchTerm) {
    const taskCards = document.querySelectorAll('.task-card');
    taskCards.forEach(card => {
        const title = card.querySelector('h6').textContent.toLowerCase();
        const description = card.querySelector('p').textContent.toLowerCase();
        
        if (title.includes(searchTerm) || description.includes(searchTerm)) {
            card.style.display = '';
        } else {
            card.style.display = 'none';
        }
    });
}

function updateTaskDetails(taskId) {
    // This function would typically make an API call to get task details
    // For now, we'll just update the UI with some placeholder animations
    const detailsPanel = document.querySelector('.task-details');
    if (detailsPanel) {
        detailsPanel.style.opacity = '0.5';
        setTimeout(() => {
            detailsPanel.style.opacity = '1';
        }, 300);
    }
}

// Update progress circles
function updateProgressCircles() {
    document.querySelectorAll('.progress-circle').forEach(circle => {
        const progress = circle.getAttribute('data-progress');
        const circumference = 2 * Math.PI * 18; // radius = 18
        const offset = circumference - (progress / 100) * circumference;
        
        const svg = `
            <svg class="progress-ring" width="40" height="40">
                <circle class="progress-ring-circle-bg" r="18" cx="20" cy="20"/>
                <circle class="progress-ring-circle" r="18" cx="20" cy="20" 
                        style="stroke-dasharray: ${circumference} ${circumference}; 
                               stroke-dashoffset: ${offset}"/>
            </svg>
            <span class="progress-text">${progress}%</span>
        `;
        
        circle.innerHTML = svg;
    });
}

// Search functionality
const searchBox = document.querySelector('.search-box');
if (searchBox) {
    searchBox.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const taskItems = document.querySelectorAll('.task-item');
        
        taskItems.forEach(item => {
            const taskTitle = item.querySelector('h6').textContent.toLowerCase();
            if (taskTitle.includes(searchTerm)) {
                item.style.display = 'flex';
            } else {
                item.style.display = 'none';
            }
        });
    });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    updateProgressCircles();
});
