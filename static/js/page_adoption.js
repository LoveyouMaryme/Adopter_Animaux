petCards = document.getElementsByClassName("pet-card");
console.log(petCards);

Array.from(petCards).forEach((element) => {
  element.addEventListener("click", () => {
    const url = element.dataset.url;

    window.location.href = url;
  });
});
