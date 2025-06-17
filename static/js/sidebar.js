document.addEventListener("DOMContentLoaded", function() {
    const sidebar = document.getElementById("sidebar");
    const toggleButtons = document.querySelectorAll("#toggleBtn, #toggleBtn-2, #close-toggle");

    if (sidebar) {
        toggleButtons.forEach(button => {
            if (button) {
                button.addEventListener("click", function() {
                    sidebar.classList.toggle("open");
                });
            }
        });
    }
});
