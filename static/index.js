let selectedLang = null; // no default selection now
let isRunning = false;

// Select language
function selectLang(lang, el) {
  selectedLang = lang;

  // remove active + checkmarks from all cards
  document.querySelectorAll(".lang-card").forEach((card) => {
    card.classList.remove("active");

    const oldCheck = card.querySelector(".checkmark");
    if (oldCheck) oldCheck.remove();
  });

  // activate clicked card
  el.classList.add("active");

  // add checkmark ONLY to selected card
  const check = document.createElement("div");
  check.className = "checkmark";
  check.textContent = "✓";
  el.appendChild(check);

  // clear error when user selects
  setStatus("", "");
}

// Start / Stop Assistant
async function toggleAssistant() {
  const btn = document.getElementById("mainBtn");

  // ❌ NO LANGUAGE SELECTED → show red error
  if (!selectedLang) {
    setStatus("Please select a language first !", "err");
    return;
  }

  if (isRunning) {
    try {
      await fetch("/stop", { method: "POST" });

      isRunning = false;

      btn.textContent = "Start Assistant";
      btn.classList.remove("running");

      setStatus("", "");
    } catch (error) {
      console.error(error);
      setStatus("Failed to stop assistant.", "err");
    }

    return;
  }

  // START
  try {
    const response = await fetch("/start", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        lang: selectedLang,
      }),
    });

    const data = await response.json();

    if (data.status === "started") {
      isRunning = true;

      btn.textContent = "Stop Assistant";
      btn.classList.add("running");

      const langLabel = selectedLang === "ar" ? "العربية" : "English";

      setStatus(`✓ Running in ${langLabel} — camera window is open`, "on");
    } else {
      setStatus("Failed to start assistant.", "err");
    }
  } catch (error) {
    console.error(error);
    setStatus("Could not connect to server. Is app.py running?", "err");
  }
}

// Status message (CENTER + STYLE CONTROL)
function setStatus(message, type) {
  let status = document.getElementById("status");

  if (!status) {
    status = document.createElement("div");
    status.id = "status";
    status.style.textAlign = "center";
    status.style.marginTop = "15px";
    document.querySelector(".card").appendChild(status);
  }

  status.textContent = message;
  status.className = `status ${type}`;
}

// Init
document.addEventListener("DOMContentLoaded", () => {
  // no default selection anymore
});
