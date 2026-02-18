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

        if (location === "All") {
            card.style.display = "block";
            return;
        }

        // Kerala = multiple cities
        if (location === "Kerala") {
            const keralaCities = [
                "Ernakulam",
                "Kozhikode",
                "Thiruvananthapuram",
                "Kannur",
                "Thrissur"
            ];

            if (keralaCities.includes(cardLocation)) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }

            return;
        }

        // Bangalore / Mangalore
        if (cardLocation.toLowerCase().includes(location.toLowerCase())) {
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
document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.getElementById("searchInput");
    const resultsBox = document.getElementById("liveResults");

    if (!searchInput || !resultsBox) {
        console.log("Search elements not found");
        return;
    }

    let allData = [];

    Promise.all([
        fetch("/api/courses").then(res => res.json()),
        fetch("/api/colleges").then(res => res.json()),
        fetch("/api/jobs").then(res => res.json())
    ]).then(([courses, colleges, jobs]) => {

        allData = [
            ...courses.map(c => ({ type: "Course", name: c.course_name, link: `/course/${c.id}` })),
            ...colleges.map(c => ({ type: "College", name: c.college_name, link: `/college/${c.id}` })),
            ...jobs.map(j => ({ type: "Job", name: j.title, link: `/job/${j.id}` }))
        ];

    }).catch(err => console.log("API fetch error:", err));

    searchInput.addEventListener("input", function () {
        const value = this.value.toLowerCase();
        resultsBox.innerHTML = "";

        if (!value) return;

        const filtered = allData
            .filter(item => item.name.toLowerCase().includes(value))
            .slice(0, 6);

        filtered.forEach(item => {
            const div = document.createElement("div");
            div.className = "live-item";
            div.innerHTML = `
                <strong>${item.name}</strong>
                <div style="font-size:12px;opacity:0.6;">${item.type}</div>
            `;
            div.onclick = () => window.location = item.link;
            resultsBox.appendChild(div);
        });
    });

});

//===== chatbot====

#chatToggle {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: #1db954;
    color: white;
    font-size: 22px;
    padding: 12px 16px;
    border-radius: 50%;
    cursor: pointer;
    box-shadow: 0 5px 20px rgba(0,0,0,0.3);
}

#chatBox {
    position: fixed;
    bottom: 80px;
    right: 20px;
    width: 300px;
    background: white;
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    padding: 10px;
}

.hidden {
    display: none;
}

.chat-header {
    font-weight: bold;
    margin-bottom: 8px;
}

#chatMessages {
    height: 200px;
    overflow-y: auto;
    margin-bottom: 10px;
    font-size: 14px;
}
