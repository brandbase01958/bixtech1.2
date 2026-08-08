// Toggle sidebar on mobile
document.addEventListener("DOMContentLoaded", () => {
  const sidebar = document.querySelector(".dash-side");
  const toggleBtn = document.createElement("button");
  sidebar.insertBefore(toggleBtn, sidebar.firstChild);

  toggleBtn.addEventListener("click", () => {
    sidebar.classList.toggle("open");
  });

  // Auto-hide flash messages
  setTimeout(() => {
    document.querySelectorAll(".flash-message").forEach(msg => msg.remove());
  }, 4000);
});

// Basic display enhancement: highlight active section when clicked
document.querySelectorAll(".dash-nav a").forEach(link => {
  link.addEventListener("click", () => {
    document.querySelectorAll(".dash-nav a").forEach(l => l.classList.remove("active"));
    link.classList.add("active");
  });
});


