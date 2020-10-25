const popUpEditTasks = document.getElementById('edit-task-pop-up');

const addTaskInput = document.querySelector('.add-task-input');
const addTaskIcon = document.getElementById('add-task-icon');


// Tasks events listener
document.addEventListener('DOMContentLoaded', (e) => {
    // add task input change icon to unchecked
    addTaskInput.addEventListener('focus', function () {
        setUncheckedIcon(addTaskIcon);
    });
    // add task input change icon to add
    addTaskInput.addEventListener('blur', function () {
        setAddIcon(addTaskIcon);
    });

    // set up tasks styles
    setAllTasksStyles();

});


// add edit tasks pop up event
document.querySelectorAll('.task-item').forEach(item => {
    item.addEventListener('contextmenu', (e) => {
        e.preventDefault();

        url = item.getElementsByTagName('a')[0];
        showPopUp(popUp = popUpEditTasks, x = e.clientX, y = e.clientY);
        delete_btn = document.getElementById('delete-task-btn');
        delete_btn.href = url.href.replace('finish_task', 'delete_task');
        return false;
    });
});

// event to listen click outside the popUp and close it
document.addEventListener('click', (e) => {
    if (popUpEditTasks.display === 'none') {
        return;
    }
    if (!popUpEditTasks.contains(e.target)) {
        hidePopUp(popUpEditTasks);
    }
});

function setAllTasksStyles() {
    // set all tasks completed or important style
    tasks.forEach(function (item) {

        var taskId = item.pk;
        var task = item.fields.task;
        var isImportant = item.fields.is_important;
        var isCompleted = item.fields.is_completed;
        task = document.getElementById(taskId);

        if (isCompleted) {
            setTaskCompleted(taskItem = task);
        }

    });
}


function setTaskCompleted(taskItem) {
    taskItem.classList.add('completed');
    icon = taskItem.getElementsByTagName('i')[0];
    setCheckedIcon(icon);
}

function setTaskUncompleted(taskItem) {
    taskItem.classList.remove('completed');
    icon = taskItem.getElementsByTagName('i')[0];
    setUncheckedIcon(icon);
}

function setUncheckedIcon(elem) {
    // set up elem icon to unchecked
    elem.textContent = 'radio_button_unchecked';
}

function setCheckedIcon(elem) {
    // set up elem icon to checked
    elem.textContent = 'check_circle';
}

function setAddIcon(elem) {
    // set up elem icon to add
    elem.textContent = 'control_point';
}
