document.addEventListener("DOMContentLoaded", () => {
  const arrowLeft = document.getElementById("arrow-left");
  const arrowRight = document.getElementById("arrow-right");
  const carouselContainer = document.getElementById("carousel-cards");

  const createAnimalCard = (pet) => {
    let imageUrl;
    if (pet.id < 8) {
      imageUrl = urlForStatic(
        "images/photo_animaux/" + pet.espece.toLowerCase() + ".jpg"
      );
    } else {
      imageUrl = urlForStatic("images/photo_animaux/default.jpg");
    }
    const calendarIconUrl = urlForStatic("images/icons/calendar.png");
    const locationIconUrl = urlForStatic("images/icons/location-pet.png");

    return `
            <div class="col-12 col-sm-6 col-lg-4 col-xl-2 d-flex flex-lg-column justify-content-center">
                <div class="pet-card bg-light d-flex flex-column w-100 h-100 p-0 pb-2 rounded-4 shadow">
                    <img
                        class="rounded-top-4 img-fluid"
                        src="${imageUrl}"
                        alt="Image de ${pet.espece}"
                    />
                    <div class="bg-light d-flex flex-column px-2">
                        <div class="d-flex flex-column mt-1">
                            <p class="name-pet mb-0 fs-4 fw-bolder text-secondary">
                                ${pet.nom}
                            </p>
                            <p class="mt-0 mb-2 fs-6 fw-light text-muted">
                                ${pet.espece}
                            </p>
                        </div>
                        <div class="icon-descr-pet d-flex flex-row gap-1 mb-1">
                            <img
                                class="img-fluid"
                                src="${calendarIconUrl}"
                                alt="Âge d'animal"
                            />
                            <p class="text-dark">${pet.age}</p>
                        </div>
                        <div class="icon-descr-pet d-flex flex-row gap-1">
                            <img
                                class="img-fluid"
                                src="${locationIconUrl}"
                                alt="Localisation"
                            />
                            <p class="text-dark">${pet.ville}</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
  };

  const updateCarousel = (animals) => {
    carouselContainer.innerHTML = "";
    animals.forEach((pet, index) => {
      const cardHTML = createAnimalCard(pet);

      carouselContainer.insertAdjacentHTML("beforeend", cardHTML);

      const newCard = carouselContainer.lastElementChild;

      newCard.classList.add("carousel-card-enter");

      setTimeout(() => {
        newCard.classList.add("active");
      }, index * 50);
    });
  };

  // Gestion de la flèche de droite
  arrowRight.addEventListener("click", async () => {
    try {
      const response = await fetch("/api/get_next_animal_carousel");
      const data = await response.json();
      updateCarousel(data);
    } catch (error) {
      console.error("Erreur lors du chargement des animaux suivants:", error);
    }
  });

  // Gestion de la flèche de gauche
  arrowLeft.addEventListener("click", async () => {
    try {
      const response = await fetch("/api/get_previous_animal_carousel");
      const data = await response.json();
      updateCarousel(data);
    } catch (error) {
      console.error("Erreur lors du chargement des animaux précédents:", error);
    }
  });
});

petCards = document.getElementsByClassName("pet-card");
console.log(petCards);

Array.from(petCards).forEach((element) => {
  element.addEventListener("click", () => {
    const url = element;
    console.log(url);

    // window.location.href = url;
  });
});
