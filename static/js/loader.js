// Show loader on page load or form submission
function showLoader() {
    const loader = document.getElementById("loader");
    if (loader) {
        loader.style.display = "flex"; // Show the loader
    }
}

// Hide loader
function hideLoader() {
    const loader = document.getElementById("loader");
    if (loader) {
        loader.style.display = "none";
    }
}

document.addEventListener("DOMContentLoaded", function () {
    // Attach loader to all form submissions except chatbot form
    const forms = document.querySelectorAll("form");
    forms.forEach(form => {
        if (form.id === "chat-form") return; // ✅ Skip loader for chatbot form

        form.addEventListener("submit", function () {
            showLoader();
        });
    });

    // Attach loader to page navigation links
    const links = document.querySelectorAll("a");
    links.forEach(link => {
        link.addEventListener("click", function (e) {
            const href = link.getAttribute("href");
            const target = link.getAttribute("target");

            // Only show loader if the link is navigating to another page
            if (href && href !== "#" && target !== "_blank" && !href.startsWith("javascript:")) {
                showLoader();
            }
        });
    });

    // Optional: Attach loader to AJAX events if your framework triggers them
    document.addEventListener("ajaxStart", showLoader);
    document.addEventListener("ajaxComplete", hideLoader);
});

// Hide loader on back/forward navigation
window.addEventListener("pageshow", function (event) {
    if (event.persisted) {
        hideLoader();
    }
});
