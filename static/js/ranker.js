// Two-step value picker: shortlist, then narrow down to the top N.
//
// Click values in the pool to add them to your shortlist — as many as you like.
// Picks beyond the target (maxPicks) are marked "over the limit"; you narrow
// down by removing them with the × button. Drag to reorder (order = rank).
// The final top-N ids are serialised into the hidden #ranked-input as a
// base64url token on every change, so the form submits the ranking.

(function () {
  "use strict";

  const pool = document.getElementById("value-pool");
  const picksList = document.getElementById("picks-list");
  const picksEmpty = document.getElementById("picks-empty");
  const countEl = document.getElementById("pick-count");
  const countWrap = countEl.parentElement;
  const hintEl = document.getElementById("picks-hint");
  const submitBtn = document.getElementById("submit-btn");
  const hiddenInput = document.getElementById("ranked-input");
  const filter = document.getElementById("value-filter");
  const maxPicks = parseInt(picksList.dataset.max, 10) || 10;

  const picks = []; // ordered array of value names (the shortlist; order = rank)

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
    const n = picks.length;
    const over = n - maxPicks;

    // Only the top maxPicks count toward the result.
    hiddenInput.value = encodeToken(picks.slice(0, maxPicks));
    countEl.textContent = String(n);
    countWrap.classList.toggle("over", over > 0);
    picksEmpty.style.display = n ? "none" : "";

    if (n === 0) {
      submitBtn.disabled = true;
      submitBtn.textContent = "Reveal my personality";
      hintEl.textContent =
        "Pick as many as resonate, then narrow to your top " + maxPicks + ".";
    } else if (over > 0) {
      submitBtn.disabled = true;
      submitBtn.textContent =
        "Remove " + over + " more to continue";
      hintEl.textContent =
        over + " over — cut the ones that matter least with ×.";
    } else {
      submitBtn.disabled = false;
      submitBtn.textContent = "Reveal my personality";
      hintEl.textContent = "Drag to rank — most important at the top.";
    }

    // Reflect chosen state on the pool chips.
    pool.querySelectorAll(".value-chip").forEach((chip) => {
      chip.classList.toggle("is-chosen", picks.includes(chip.dataset.name));
    });
  }

  function render() {
    picksList.innerHTML = "";
    picks.forEach((name, idx) => {
      // Divider between the keepers (top maxPicks) and the ones to cut.
      if (idx === maxPicks) {
        const divider = document.createElement("li");
        divider.className = "cut-divider";
        divider.setAttribute("aria-hidden", "true");
        divider.textContent = "↑ your top " + maxPicks + " · cut below ↓";
        picksList.appendChild(divider);
      }

      const li = document.createElement("li");
      li.className = "pick-item" + (idx >= maxPicks ? " over-limit" : "");
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
    if (picks.includes(name)) return;
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

  // Restore a ranking passed in via the URL token, so shared/bookmarked links —
  // and "edit your choices" — repopulate the picks in order.
  const initial = (picksList.dataset.initial || "")
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
  initial.forEach(addPick);

  sync();
})();
