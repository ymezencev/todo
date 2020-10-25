
const popUpEditCategories = document.getElementById('edit-category-pop-up');
const hideCategoriesBtn = document.getElementById('hide-categories-btn');
const tasksTitle = document.querySelector('.tasks .title');

// Categories events listener
document.addEventListener('DOMContentLoaded', (e) => {
    highlightCurrentCategoryMenu();
    autoHideCategories();
});


// hide categories
hideCategoriesBtn.addEventListener('click', (e) => {
    hideCategories();
});

function hideCategories() {
    // hide left menu
    let categoriesClassList = document.querySelector('.categories').classList;
    let isHidden = categoriesClassList.contains('hidden') === true;
    categoriesClassList.toggle("hidden");
    localStorage.setItem("isCategoriesHidden", !isHidden);
}

function autoHideCategories() {
    // check if the option hide menu was chosen and hide menu if needed
    const isCategoriesHidden = localStorage.getItem("isCategoriesHidden");
    if (isCategoriesHidden === 'true') {
        hideCategories();
    }
}

function highlightCurrentCategoryMenu() {
    // highlights current category page in the menu bar
    let currentURL = window.location.href;

    document.querySelectorAll('.categories a').forEach(item => {
        if(currentURL.indexOf(item.getAttribute('href')) !== -1){
            item.classList.add('active');
            let name = item.getElementsByTagName('span')[0].textContent;
            tasksTitle.innerHTML = name + '<br>' + new Date().toDateString();
        }
    });
}


// add edit categories pop up event
document.querySelectorAll('.custom-category').forEach(item => {
    item.addEventListener('contextmenu', (e) =>{
        e.preventDefault();

        showPopUp(popUp=popUpEditCategories, x=e.clientX, y=e.clientY);
        delete_btn = document.getElementById('delete-category-btn');
        delete_btn.href = item.href + 'delete_category';
        return false;
    });
});

// event to listen click outside the popUp and close it
document.addEventListener('click', (e) => {
    if (popUpEditCategories.display === 'none') {
        return;
    }

    if (!popUpEditCategories.contains(e.target)) {
        hidePopUp(popUpEditCategories);
    }
});