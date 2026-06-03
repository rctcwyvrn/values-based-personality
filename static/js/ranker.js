// Drag-to-rank value picker.
//
// Clicking a value in the pool adds it to the ordered picks list (up to max).
// Picks can be reordered by drag-and-drop and removed by clicking the x.
// The ordered names are serialised into the hidden #ranked-input on every
// change, so the form submits a comma-separated ranking.

(function () {
  "use strict";

  const pool = document.getElementById("value-pool");
  const picksList = document.getElementById("picks-list");
  const picksEmpty = document.getElementById("picks-empty");
  const countEl = document.getElementById("pick-count");
  const submitBtn = document.getElementById("submit-btn");
  const hiddenInput = document.getElementById("ranked-input");
  const filter = document.getElementById("value-filter");
  const maxPicks = parseInt(picksList.dataset.max, 10) || 10;

  const picks = []; // ordered array of value names

  // name -> stable value id, read from the rendered chips. The ranking is
  // submitted as a base64url token of these ids (one byte each), matching the
  // server's encoding, rather than a comma-separated list of names.
  const idOf = {};
  pool.querySelectorAll(".value-chip").forEach((chip) => {
    idOf[chip.dataset.name] = parseInt(chip.dataset.id, 10);
  });

  function encodeToken(names) {
    let bin = "";
    names.forEach((name) => {
      const id = idOf[name];
      if (id >= 0) bin += String.fromCharCode(id);
    });
    if (!bin) return "";
    return btoa(bin).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  }

  function sync() {
    hiddenInput.value = encodeToken(picks);
    countEl.textContent = String(picks.length);
    submitBtn.disabled = picks.length === 0;
    picksEmpty.style.display = picks.length ? "none" : "";

    // Reflect chosen state on the pool chips.
    pool.querySelectorAll(".value-chip").forEach((chip) => {
      const chosen = picks.includes(chip.dataset.name);
      chip.classList.toggle("is-chosen", chosen);
    });
  }

  function render() {
    picksList.innerHTML = "";
    picks.forEach((name, idx) => {
      const li = document.createElement("li");
      li.className = "pick-item";
      li.draggable = true;
      li.dataset.name = name;

      const rank = document.createElement("span");
      rank.className = "pick-rank";
      rank.textContent = String(idx + 1);

      const label = document.createElement("span");
      label.className = "pick-name";
      label.textContent = name;

      const remove = document.createElement("button");
      remove.type = "button";
      remove.className = "pick-remove";
      remove.setAttribute("aria-label", "Remove " + name);
      remove.textContent = "×";
      remove.addEventListener("click", () => {
        const i = picks.indexOf(name);
        if (i !== -1) picks.splice(i, 1);
        render();
        sync();
      });

      li.append(rank, label, remove);
      attachDrag(li);
      picksList.appendChild(li);
    });
  }

  function addPick(name) {
    if (picks.includes(name) || picks.length >= maxPicks) return;
    picks.push(name);
    render();
    sync();
  }

  // --- drag and drop reordering --------------------------------------------
  let dragName = null;

  function attachDrag(li) {
    li.addEventListener("dragstart", (e) => {
      dragName = li.dataset.name;
      li.classList.add("dragging");
      e.dataTransfer.effectAllowed = "move";
    });
    li.addEventListener("dragend", () => {
      li.classList.remove("dragging");
      dragName = null;
    });
    li.addEventListener("dragover", (e) => {
      e.preventDefault();
      const overName = li.dataset.name;
      if (!dragName || dragName === overName) return;
      const from = picks.indexOf(dragName);
      const to = picks.indexOf(overName);
      if (from === -1 || to === -1) return;
      picks.splice(to, 0, picks.splice(from, 1)[0]);
      render();
      sync();
      // keep dragging the same item
      const moved = picksList.querySelector('[data-name="' + cssEscape(dragName) + '"]');
      if (moved) moved.classList.add("dragging");
    });
  }

  function cssEscape(s) {
    return (window.CSS && CSS.escape) ? CSS.escape(s) : s.replace(/"/g, '\\"');
  }

  // --- pool interactions ---------------------------------------------------
  pool.addEventListener("click", (e) => {
    const chip = e.target.closest(".value-chip");
    if (chip) addPick(chip.dataset.name);
  });
  pool.addEventListener("keydown", (e) => {
    if (e.key !== "Enter" && e.key !== " ") return;
    const chip = e.target.closest(".value-chip");
    if (chip) {
      e.preventDefault();
      addPick(chip.dataset.name);
    }
  });

  filter.addEventListener("input", () => {
    const q = filter.value.trim().toLowerCase();
    pool.querySelectorAll(".value-chip").forEach((chip) => {
      const hay = chip.dataset.name.toLowerCase() + " " +
        chip.querySelector(".chip-desc").textContent.toLowerCase();
      chip.style.display = hay.includes(q) ? "" : "none";
    });
  });

  // Restore a ranking passed in via the URL (?ranked=A,B,C), so shared and
  // bookmarked links — and "edit your choices" — repopulate the picks in order.
  const initial = (picksList.dataset.initial || "")
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
  initial.forEach(addPick);

  sync();
})();
