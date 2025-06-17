

function openInputPage() {
  const equipmentCardContainer = document.getElementById('equipment-card-container');
  const inputFormContainer = document.getElementById('input-form-container');

  // Hide the equipment card and show the input form with smooth transitions
  equipmentCardContainer.style.display = 'none';
  inputFormContainer.style.display = 'flex';
  inputFormContainer.style.justifyContent = 'center';
  inputFormContainer.style.width = '100%';
  
  // Optional: Add smooth transitions by changing opacity
  inputFormContainer.style.opacity = 0;
  setTimeout(() => {
      inputFormContainer.style.transition = 'opacity 0.5s ease';
      inputFormContainer.style.opacity = 1;
  }, 10);  // Delay for ensuring the transition takes effect
}


document.addEventListener('DOMContentLoaded', function() {
  var searchBar = document.getElementById('search-bar');

  if (searchBar) {

      var isAboutPage = window.location.pathname === "/about";
      // Check if the page is index.html
      if (window.location.pathname === "/content") {
          searchBar.style.display = 'block';  // Show the button only on index.html
      }
      else {
          searchBar.style.display = 'none';  // Hide on other pages
      }
  }
});




//Top Nav bar
document.addEventListener("DOMContentLoaded", () => {
  const topbar = document.getElementById("topbar-r");
  const toggleSvg = document.querySelector(".topbar-toggle");

  // Toggle active class when SVG is clicked
  toggleSvg.addEventListener("click", (event) => {
      event.preventDefault(); // Prevent default behavior
      topbar.classList.toggle("active");
      toggleSvg.classList.toggle("active");
  });

  // Close topbar when clicking anywhere outside it
  document.addEventListener("click", (event) => {
      // Check if the click is outside the topbar or the toggle SVG
      if (!topbar.contains(event.target) && event.target !== toggleSvg) {
          topbar.classList.remove("active");
          toggleSvg.classList.remove("active");
      }
  });
});
