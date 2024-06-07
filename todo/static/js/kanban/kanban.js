function allowDrop(event) {
    event.preventDefault();
}

function drag(event) {
    event.dataTransfer.setData('text/plain', event.target.id);
}

function drop(event) {
    event.preventDefault();
    var taskId = event.dataTransfer.getData('text/plain').split('-')[1];
    var newStatus = event.currentTarget.dataset.status;
    var csrfToken = getCSRFToken();
    updateTaskStatus(taskId, newStatus, csrfToken);
}

function updateTaskStatus(taskId, newStatus, csrfToken) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/update-task-status/');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', csrfToken);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.onload = function() {
        if (xhr.status === 200) {
            var responseData = JSON.parse(xhr.responseText);
            updateUI(responseData);
            assignEventHandlers();
        }
    };
    xhr.send(JSON.stringify({ taskId: taskId, newStatus: newStatus }));
}

function updateUI(data) {
    updateColumn('todo-list', data.todo_tasks);
    updateColumn('doing-list', data.doing_tasks);
    updateColumn('done-list', data.done_tasks);
}

function updateColumn(columnId, tasks) {
    var column = document.getElementById(columnId);
    column.innerHTML = '';
    tasks.forEach(function(task) {
        var taskItem = document.createElement('li');
        taskItem.className = 'task-item';
        taskItem.draggable = true;
        taskItem.id = 'task-' + task.id;
        taskItem.innerHTML = '<i class="fas fa-circle"></i><span>' + task.title + '</span>';
        column.appendChild(taskItem);
    });
}

function assignEventHandlers() {
    var taskItems = document.querySelectorAll('.task-item');
    taskItems.forEach(function(taskItem) {
        taskItem.addEventListener('dragstart', drag);
    });

    var columns = document.querySelectorAll('.column');
    columns.forEach(function(column) {
        column.addEventListener('drop', drop);
        column.addEventListener('dragover', allowDrop);
    });
}

function getCSRFToken() {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.startsWith('csrftoken=')) {
            return cookie.substring('csrftoken='.length, cookie.length);
        }
    }
    return null;
}

assignEventHandlers();
