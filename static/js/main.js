console.log("main.js loaded");

/* ===========================
   THEME TOGGLE (GLOBAL)
=========================== */

function toggleTheme() {
    document.body.classList.toggle("dark");

    const theme = document.body.classList.contains("dark") ? "dark" : "light";
    localStorage.setItem("theme", theme);
}

window.addEventListener("load", () => {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
        document.body.classList.add("dark");
    }
});

/* ===========================
   COLLEGE FILTER (STATIC PAGE)
=========================== */

function filterColleges(location, element) {
    const cards = document.querySelectorAll(".college-card");
    const tabs = document.querySelectorAll(".category");

    tabs.forEach(tab => tab.classList.remove("active"));
    element.classList.add("active");

    cards.forEach(card => {
        const cardLocation = card.dataset.location;

        if (location === "All" || cardLocation === location) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }
    });
}

// =====================
// Stats Counter Animation
// =====================

document.addEventListener("DOMContentLoaded", function () {

    const counters = document.querySelectorAll(".counter");
    const statsSection = document.querySelector(".stats");
    let animationStarted = false;

    function startCounterAnimation() {
        if (animationStarted) return;
        animationStarted = true;

        counters.forEach(counter => {
            const target = +counter.getAttribute("data-target");
            let count = 0;
            const increment = target / 100;

            function updateCount() {
                count += increment;

                if (count < target) {
                    counter.innerText = Math.ceil(count) + "+";
                    requestAnimationFrame(updateCount);
                } else {
                    counter.innerText = target + "+";
                }
            }

            updateCount();
        });

        // Show animation fade effect
        document.querySelectorAll(".stat").forEach(stat => {
            stat.classList.add("show");
        });
    }

    window.addEventListener("scroll", function () {
        const sectionTop = statsSection.getBoundingClientRect().top;

        if (sectionTop < window.innerHeight - 100) {
            startCounterAnimation();
        }
    });

});
