

function setErrorFor(input, message) {
    const formControl = input.parentElement; // .form-control div
    const smallLabel = formControl.querySelector('small');
    smallLabel.innerText = message;
    formControl.className = 'form-control error';
}

function setSuccessFor(input) {
    const formControl = input.parentElement; // .form-control div
    const smallLabel = formControl.querySelector('small');
    smallLabel.innerText = '';
    formControl.className = 'form-control success';
}

function CheckEmail(email) {
    return /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(email);
}
