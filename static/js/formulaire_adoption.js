const inputs = document.getElementsByClassName("form-control");
// const form = document.getElementById("form");

const nomAnimal = document.getElementById("petNameInput");
const address = document.getElementById("streetInput");
const codePostal = document.getElementById("postalCodeInput");
const ageAnimal = document.getElementById("petAgeInput");
const city = document.getElementById("cityInput");

// console.log(pictureAnimal);

function checkNameCharacters(input) {
  const value = input.value.trim();

  if (value.length >= 3 && value.length <= 20 && !value.includes(",")) {
    input.classList.add("is-valid");
    input.classList.remove("is-invalid");
  } else {
    input.classList.add("is-invalid");
    input.classList.remove("is-valid");
  }
}

function checkEmpty(input) {
  const value = input.value.trim();

  if (value !== "") {
    input.classList.add("is-valid");
    input.classList.remove("is-invalid");
  } else {
    input.classList.add("is-invalid");
    input.classList.remove("is-valid");
  }
}

function checkAge(input) {
  const value = parseInt(input.value.trim(), 10);

  if (!isNaN(value) && value >= 0 && value <= 20) {
    input.classList.add("is-valid");
    input.classList.remove("is-invalid");
  } else {
    input.classList.add("is-invalid");
    input.classList.remove("is-valid");
  }
}

function checkPostalCode(input) {
  const value = input.value.trim().toUpperCase();
  const regex = /^[A-Z]\d[A-Z][ ]?\d[A-Z]\d$/;

  input.classList.remove("is-valid", "is-invalid");

  if (regex.test(value)) {
    input.classList.add("is-valid");
  } else {
    input.classList.add("is-invalid");
  }
}

function checkAddressName(input) {
  const value = input.value.trim().toUpperCase();
  const regex = /^[0-9]+\s+[A-ZÀ-Ö' -]+$/;

  input.classList.remove("is-valid", "is-invalid");
  input.setCustomValidity("");

  if (regex.test(value)) {
    input.classList.add("is-valid");
  } else {
    input.classList.add("is-invalid");
  }
}

function checkCity(input) {
  const value = input.value.trim().toUpperCase();
  const regex = /^[A-ZÀ-Ö' -]+$/;

  input.classList.remove("is-valid", "is-invalid");
  input.setCustomValidity("");

  if (regex.test(value)) {
    input.classList.add("is-valid");
  } else {
    input.classList.add("is-invalid");
  }
}
var forms = document.getElementsByClassName("needs-validation");
// Loop over them and prevent submission
var validation = Array.prototype.filter.call(forms, function (form) {
  form.addEventListener(
    "submit",
    function (event) {
      Array.from(inputs).forEach((input) => {
        checkEmpty(input);
      });

      checkAge(ageAnimal);
      checkNameCharacters(nomAnimal);
      checkPostalCode(codePostal);
      checkAddressName(address);
      checkCity(city);

      if (form.checkValidity() === false) {
        event.preventDefault();
        event.stopPropagation();
      }
    },
    false
  );
});
