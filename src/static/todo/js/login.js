const form = document.getElementById('form');
const username = document.getElementById('id_username');
const password = document.getElementById('id_password');

let isFormValid = true;

let postValidationErrors = errors;


document.addEventListener('DOMContentLoaded', (e) => {
    if (Object.keys(postValidationErrors).length !== 0) {
        CheckAllInputs();
    }
});

form.addEventListener('submit', (e) => {
    CheckAllInputs();
    if (!isFormValid) {
        e.preventDefault();

    }
});

username.addEventListener('blur', (e) => CheckInputUsername(), true);
password.addEventListener('blur', (e) => CheckInputPassword(), true);

function CheckInputUsername() {
    const usernameValue = username.value.trim();

    if (usernameValue === '') {
        setErrorFor(username, 'Username cannot be blank.');
        isFormValid = false;
    } else {
        setSuccessFor(username);
    }
}

function CheckInputPassword() {
    const passwordValue = password.value.trim();

    if (postValidationErrors['invalid_login']) {
        setErrorFor(password, postValidationErrors['invalid_login']);
        delete postValidationErrors['invalid_login'];
        isFormValid = false;
    } else if (passwordValue === '') {
        setErrorFor(password, 'Password cannot be blank.');
        isFormValid = false;
    } else {
        setSuccessFor(password);
    }
}

function CheckAllInputs() {
    isFormValid = true;
    CheckInputUsername();
    CheckInputPassword();
}

