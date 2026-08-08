document.addEventListener("DOMContentLoaded", () => {
  // --- Progress bar tracking ---
  const progressBar = document.getElementById("task-progress-bar");
  const progressLabel = document.getElementById("task-progress-label");

  if (progressBar && progressLabel) {
    // Values are already rendered by Django into the HTML
    const completed = parseInt(progressLabel.textContent.split(" ")[0]) || 0;
    const total = parseInt(progressLabel.textContent.split(" ")[2]) || 0;
    const percent = total > 0 ? Math.round((completed / total) * 100) : 0;

    progressBar.style.width = percent + "%";
    progressLabel.textContent = `${completed} of ${total} tasks complete (${percent}%)`;
  }

  // --- Task checkbox interaction ---
  document.querySelectorAll(".task-item input[type='checkbox']").forEach(cb => {
    cb.addEventListener("change", () => {
      const title = cb.closest(".task-item").querySelector(".t-title").textContent;
      const status = cb.checked ? "complete" : "in progress";

      // Update the meta text visually
      const meta = cb.closest(".task-item").querySelector(".t-meta");
      const dueText = meta.textContent.split("·")[0]; // keep "Due ..."
      meta.textContent = `${dueText} · ${status}`;

      // Optionally send update back to server via fetch
      fetch("/dashboard/update-task-status/", {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ title, status })
      }).catch(err => console.error("Task update failed:", err));
    });
  });

  // --- Sidebar nav highlight ---
  document.querySelectorAll(".dash-nav a").forEach(link => {
    link.addEventListener("click", () => {
      document.querySelectorAll(".dash-nav a").forEach(l => l.classList.remove("active"));
      link.classList.add("active");
    });
  });

  // --- Utility: get CSRF token ---
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
