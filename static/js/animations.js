document.addEventListener("DOMContentLoaded", function () {
    const elements = document.querySelectorAll(".fade-in");

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add("visible");
                }, index * 200); // Delay increases for each element
                observer.unobserve(entry.target); // Stop observing once visible
            }
        });
    }, { threshold: 0.7 }); // Trigger when 0.x*100 of element is visible

    elements.forEach((el) => observer.observe(el));
});

document.addEventListener("DOMContentLoaded", function () {
    // Select all elements that should have the click effect
    const clickableElements = document.querySelectorAll(".click-effect");

    clickableElements.forEach(element => {
        element.addEventListener("click", function () {
            element.classList.add("clicked");

            setTimeout(() => {
                element.classList.remove("clicked");
            }, 200); // Removes the class after the animation
        });
    });
});


const floatingElements = document.querySelectorAll('.floating');

// Assign staggered delay
floatingElements.forEach((el, index) => {
  el.style.animationDelay = `${index * 0.3}s`; // 0.3s between each
});

let isScrolling;

window.addEventListener('scroll', () => {
  floatingElements.forEach(el => {
    el.classList.add('floating-disturbed');
  });

  clearTimeout(isScrolling);

  isScrolling = setTimeout(() => {
    floatingElements.forEach(el => {
      el.classList.remove('floating-disturbed');
    });
  }, 300); // delay before resuming animation
});

