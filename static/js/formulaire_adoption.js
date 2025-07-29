const inputs = document.getElementsByClassName("form-control");
const form = document.getElementById("form");

const nomAnimal = document.getElementById("petNameInput");
const ageAnimal = document.getElementById("petAgeInput");
const codePostalInput = document.getElementById("postalCodeInput");
const pictureAnimal = document.getElementById("petFileInput");

console.log(pictureAnimal);

// Boucle qui assigne un listener à chaque champ
Array.from(inputs).forEach((input) => {
  input.addEventListener("input", () => {
    if (input.id === "petNameInput") {
      checkNameCharacters(input);
    } else if (input.id === "petAgeInput") {
      checkAge(input);
    } else if (input.id === "postalCodeInput") {
      checkPostalCode(input);
    } else if (input.id === "petFileInput") {
      checkPicture(input);
    } else {
      checkVirgule(input);
    }

    input.id;
  });
});

pictureAnimal.addEventListener("click", () => {
  console.log("clicked");
  checkPicture(pictureAnimal);
});

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

function checkVirgule(input) {
  const value = input.value.trim();

  if (value !== "" && !value.includes(",")) {
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

  if (regex.test(value)) {
    input.classList.add("is-valid");
    input.classList.remove("is-invalid");
  } else {
    input.classList.add("is-invalid");
    input.classList.remove("is-valid");
  }
}

function checkPicture(input) {
  if (input.files.length > 0) {
    console.log("valid");
    input.classList.add("is-valid");
    input.classList.remove("is-invalid");
  } else {
    console.log("invalid");
    input.classList.add("is-invalid");
    input.classList.remove("is-valid");
  }
}

form.addEventListener("submit", function (event) {
  if (!form.checkValidity()) {
    event.preventDefault();
    event.stopPropagation();
  }

  form.classList.add("was-validated");
});
