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

const formBid = document.querySelector("#bid_form");
const buttonBid = formBid.querySelector("input[type='submit']");
const inputPriceBid = document.querySelector("input[name='price']");
const labelPrice = formBid.querySelector("label[for='id_price']");
formBid.className = "d-inline-flex align-items-center m-2"
labelPrice.className = "mb-0 mr-2"
inputPriceBid.className = "form-control";
const divInputGroup = document.createElement("div");
divInputGroup.className = "input-group";
const divInputGroupPrepend = document.createElement("div");
divInputGroupPrepend.className = "input-group-prepend";
const divInputGroupText = document.createElement("div");
divInputGroupText.className = "input-group-text";
divInputGroupText.innerText = "$"
buttonBid.before(divInputGroup);
divInputGroup.appendChild(divInputGroupPrepend);
divInputGroup.appendChild(inputPriceBid);
divInputGroupPrepend.appendChild(divInputGroupText);
divInputGroup.style.height = '100%';
divInputGroup.style.minWidth = '150px';
buttonBid.style.height = '38px';
buttonBid.style.marginBottom = '0';
labelPrice.style.width = '30%';


