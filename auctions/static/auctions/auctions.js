const inputRegister = document.querySelectorAll("form#register_form input");
const labelRegister = document.querySelectorAll("form#register_form label");

inputRegister.forEach((el) => {
    if (el.type !== "submit") {
        el.className = 'form-control'
    }
})

labelRegister.forEach((el) => {
    el.className = "sr-only"
})
