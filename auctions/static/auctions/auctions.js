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

const eyeFill = document.querySelector("a#eye-fill");
const eye = document.querySelector("a#eye");

eye.addEventListener('mouseover', (el) => {
    el.target.innerHtml = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"28\" height=\"28\" fill=\"currentColor\" className=\"bi bi-eye-fill\"\n" +
        "             viewBox=\"0 0 16 16\">\n" +
        "            <path d=\"M10.5 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0z\"/>\n" +
        "            <path d=\"M0 8s3-5.5 8-5.5S16 8 16 8s-3 5.5-8 5.5S0 8 0 8zm8 3.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z\"/>\n" +
        "        </svg>"


})