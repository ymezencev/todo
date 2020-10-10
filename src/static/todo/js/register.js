const form = document.getElementById('form');
const username = document.getElementById('id_username');
const email = document.getElementById('id_email');
const password1 = document.getElementById('id_password1');
const password2 = document.getElementById('id_password2');

let isFormValid = true;

let postValidationErrors = errors;

username.placeholder = 'todo_user17';
email.placeholder = 'user@todo.com';
password1.placeholder = 'Enter password';
password2.placeholder = 'Check Password';

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
email.addEventListener('blur', (e) => CheckInputEmail(), true);
password1.addEventListener('blur', (e) => CheckInputPassword1(), true);
password2.addEventListener('blur', (e) => CheckInputPassword2(), true);

function CheckInputUsername() {
    const usernameValue = username.value.trim();

    if (postValidationErrors['username']) {
        setErrorFor(username, postValidationErrors['username'][0]['message']);
        username.value = '';
        delete postValidationErrors['username'];
        isFormValid = false;
    } else if (usernameValue === '') {
        setErrorFor(username, 'Username cannot be blank.');
        isFormValid = false;
    } else {
        setSuccessFor(username);
    }
}

function CheckInputEmail() {
    const emailValue = email.value.trim();

    if (postValidationErrors['email']) {
        setErrorFor(email, postValidationErrors['email'][0]['message']);
        delete postValidationErrors['email'];
        isFormValid = false;
    } else if (emailValue === '') {
        setErrorFor(email, 'Email cannot be blank.');
        isFormValid = false;
    } else if (!CheckEmail(emailValue)) {
        setErrorFor(email, 'Email is not valid.');
        isFormValid = false;
    } else {
        setSuccessFor(email);
    }
}

function CheckInputPassword1() {
    const password1Value = password1.value.trim();
    if (password1Value === '') {
        setErrorFor(password1, 'Password cannot be blank.');
        isFormValid = false;
    } else {
        setSuccessFor(password1);
    }
}

function CheckInputPassword2() {
    const password1Value = password1.value.trim();
    const password2Value = password2.value.trim();

    if (postValidationErrors['password2']) {
        setErrorFor(password2, postValidationErrors['password2'][0]['message']);
        setErrorFor(password1, 'Password cannot be blank.');
        delete postValidationErrors['password2'];
        isFormValid = false;
    } else if (password2Value === '') {
        setErrorFor(password2, 'Password cannot be blank.');
        isFormValid = false;
    } else if (password2Value !== password1Value) {
        setErrorFor(password2, 'Passwords does not match.');
        isFormValid = false;
    } else {
        setSuccessFor(password2);
    }
}

function CheckAllInputs() {
    isFormValid = true;
    CheckInputUsername();
    CheckInputEmail();
    CheckInputPassword1();
    CheckInputPassword2();
}

