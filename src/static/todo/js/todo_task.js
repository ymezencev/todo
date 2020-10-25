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


// add event listener to every task
document.querySelectorAll('.task-item').forEach(item => {
    // edit popUp
    addEditPopUpListener(item);
});


// add edit popUp listener to the passed taskItem
function addEditPopUpListener(taskItem){
    taskItem.addEventListener('contextmenu', (e) => {
        e.preventDefault();
        let url = taskItem.getElementsByTagName('a')[0];
        showPopUp(popUp = popUpEditTasks, x = e.clientX, y = e.clientY);
        let delete_btn = document.getElementById('delete-task-btn');
        delete_btn.href = url.href.replace('finish_task', 'delete_task');
        return false;
    });
}

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

        let taskId = item.pk;
        let taskText = item.fields.task;
        let isImportant = item.fields.is_important;
        let isCompleted = item.fields.is_completed;
        let task = document.getElementById(taskId);

        if (isCompleted) {
            setTaskCompleted(taskItem = task);
        }

        if (isImportant) {
            setTaskImportant(taskItem = task);
            setNotImportantHref(taskItem = task);
        }
    });
}

function setNotImportantHref(taskItem){
    // if task is important - change url to not important
    const importantBtn = taskItem.querySelector('.important-btn');
    importantBtn.href = importantBtn.href.replace(
        'set_task_important',
        'set_task_not_important');

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

function setTaskImportant(taskItem) {
    taskItem.classList.add('important');
    icon = taskItem.getElementsByTagName('i')[1]; // second i tag
    setImportantIcon(icon);
}

function setTaskNotImportant(taskItem) {
    taskItem.classList.remove('important');
    icon = taskItem.getElementsByTagName('i')[1]; // second i tag
    setNotImportantIcon(icon);
}

// Set icons //
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

function setImportantIcon(elem) {
    // set up elem icon to important star
    elem.textContent = 'star';
}
function setNotImportantIcon(elem) {
    // set up elem icon to not important star
    elem.textContent = 'star_border';
}
