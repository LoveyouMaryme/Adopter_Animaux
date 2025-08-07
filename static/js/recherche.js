//  Variables
const button_especes = document.getElementsByClassName("button_espece");
const container_button_race = document.getElementById("container-button-race");
const container_results = document.getElementById("container-results");
const search_button = document.getElementById("search-button");
const searchBar = document.getElementById("searchBar");

// Functions

// Permet de rendre le bouton actif
function toggleButton(button) {
  button.classList.toggle("active");
}

// Permet de append ensemble les actif button de especes pour le url
function getSelectedParamString(isEspeces = false) {
  console.log("c'est mes races ca");
  console.log(isEspeces);
  const prefix = isEspeces ? "especes" : "races";
  return getActiveButtons(isEspeces)
    .map((val) => `${prefix}=${val}`)
    .join("&");
}

// Get tous les actifs buttons de especes ou de races
function getActiveButtons(isEspeces = false) {
  const className = isEspeces ? "button_espece" : "button-race";
  return Array.from(document.getElementsByClassName(`${className} active`)).map(
    (btn) => btn.textContent.toLowerCase().trim()
  );
}

// Appel le call api avec les ParamsString construits
function fetchRacesForActiveEspeces() {
  const especeParamString = getSelectedParamString(true);
  let url;

  if (especeParamString.includes("especes=tous")) {
    url = "http://127.0.0.1:5000/api/races?especes=*";
  } else {
    url = "http://127.0.0.1:5000/api/races?" + especeParamString;
  }

  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      updateRaces(data);
      console.log(data);
      return data;
    })
    .catch((error) => {
      console.error("Erreur de requête :", error.message);
    });
}

// Quand bouton espece cliqué update les boutons races en les supprimant puis les recréant
function updateRaces(apiData) {
  while (container_button_race.childNodes.length > 2) {
    container_button_race.removeChild(container_button_race.lastChild);
  }

  apiData.forEach((elementData) => {
    if (elementData != "Inconnu") {
      const newButton = document.createElement("button");
      newButton.classList.add(
        "btn",
        "btn-outline-primary",
        "rounded-pill",
        "button-race"
      );
      newButton.textContent = elementData;

      newButton.addEventListener("click", async () => {
        toggleButton(newButton);
        const apiResults = await displayResults();
        updateResults(apiResults);
      });

      container_button_race.appendChild(newButton);
    }
  });
}

function fetchResults(url) {
  return fetch(url)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log(data);
      return data;
    })
    .catch((error) => {
      console.error(error.message);
      return [];
    });
}

// Crée le nouveau lien avec les choix de races et especes
async function displayResults() {
  let url_results = "http://127.0.0.1:5000/api/results?";
  const especeParam = getSelectedParamString(true);
  const raceParam = getSelectedParamString(false);
  console.log("Mes races params");
  console.log(raceParam);
  const filters = [];

  if (
    especeParam.includes("especes=*") ||
    especeParam.includes("especes=tous")
  ) {
    filters.push("especes=*");
  } else if (especeParam) {
    filters.push(especeParam);
  }

  if (raceParam.includes("races=*") || raceParam.includes("races=tous")) {
    filters.push("races=*");
  } else if (raceParam) {
    filters.push(raceParam);
  }

  url_results += filters.join("&");
  console.log(url_results);

  return await fetchResults(url_results);
}

function updateResults(results) {
  container_results.innerHTML = "";

  if (results.length === 0) {
    container_results.innerHTML =
      "<p class='text-muted'>Aucun résultat trouvé.</p>";
    return;
  }

  results.forEach((element) => {
    const [nom, espece, race, ville] = element;

    const new_li = document.createElement("li");
    new_li.classList.add("mb-2", "p-2", "border", "rounded");

    new_li.innerHTML = `
      <strong>${nom}</strong><br>
      <span class="text-secondary">${espece}</span> -
      <span>${race}</span><br>
      <i class="bi bi-geo-alt-fill me-1"></i>
      <span>${ville}</span>
    `;

    container_results.appendChild(new_li);
  });
}

// call this when the user submits or on keypress, etc.
async function searchbarResult() {
  // 1. grab the raw string from your input
  const searchBar = document.getElementById("searchBar");
  const words = searchBar.value.trim();
  console.log(words);

  const wordList = words.split(/\s+/);

  console.log(wordList);

  const baseUrl = "http://127.0.0.1:5000/api/results_searchbar";
  const filters = wordList.map((word) => `filters=${word}`);
  const queryString = filters.join("&");
  const finalUrl = `${baseUrl}?${queryString}`;

  const data = await fetchResults(finalUrl);
  return data;
}

// Event Listeners
Array.from(button_especes).forEach((button) => {
  button.addEventListener("click", async () => {
    toggleButton(button);
    fetchRacesForActiveEspeces();
    const apiResults = await displayResults();
    updateResults(apiResults);
  });
});

search_button.addEventListener("click", async () => {
  const searchBarResult = await searchbarResult();
  updateResults(searchBarResult);
});

searchBar.addEventListener("keydown", async (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    const searchBarResult = await searchbarResult();
    updateResults(searchBarResult);
  }
});
