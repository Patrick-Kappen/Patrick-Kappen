const filter = document.querySelector("[data-work-filter]");
const list = document.querySelector("[data-work-list]");
const empty = document.querySelector("[data-work-empty]");

if (filter && list) {
  const buttons = [...filter.querySelectorAll("[data-filter]")];
  const entries = [...list.querySelectorAll("[data-tags]")];

  const apply = (value) => {
    let shown = 0;
    for (const entry of entries) {
      const match = !value || entry.dataset.tags.split(" ").includes(value);
      entry.hidden = !match;
      if (match) shown += 1;
    }
    for (const button of buttons) {
      button.setAttribute("aria-pressed", String(button.dataset.filter === value));
    }
    if (empty) empty.hidden = shown > 0;
  };

  filter.addEventListener("click", (event) => {
    const button = event.target.closest("[data-filter]");
    if (!button) return;
    const value = button.dataset.filter;
    apply(value);
    const url = new URL(window.location.href);
    if (value) url.searchParams.set("tag", value);
    else url.searchParams.delete("tag");
    history.replaceState(null, "", url);
  });

  filter.hidden = false;
  const initial = new URL(window.location.href).searchParams.get("tag") ?? "";
  apply(buttons.some((button) => button.dataset.filter === initial) ? initial : "");
}
