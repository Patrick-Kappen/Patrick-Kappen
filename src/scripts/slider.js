for (const button of document.querySelectorAll("[data-slide]")) {
  const slider = button.closest(".topics-panel")?.querySelector("[data-slider]");
  if (!slider) continue;

  button.addEventListener("click", () => {
    const card = slider.querySelector("li");
    const step = card ? card.getBoundingClientRect().width + 24 : slider.clientWidth;
    slider.scrollBy({ left: button.dataset.slide === "next" ? step : -step, behavior: "smooth" });
  });
}
