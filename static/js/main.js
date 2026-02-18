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


// ===== CHATBOT =====

document.addEventListener("DOMContentLoaded", function () {

    const chatToggle = document.getElementById("chatToggle");
    const chatBox = document.getElementById("chatBox");
    const chatInput = document.getElementById("chatInput");
    const chatMessages = document.getElementById("chatMessages");

    if (!chatToggle || !chatBox) return;

    // Toggle chat
    chatToggle.addEventListener("click", () => {
        chatBox.classList.toggle("hidden");
    });

    // Send on Enter
    chatInput.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            sendMessage();
        }
    });

    function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;

        addMessage("You", message);
        chatInput.value = "";

        showTyping();

        setTimeout(() => {
            removeTyping();
            const reply = getBotResponse(message);
            addMessage("Bot", reply);
        }, 1200);
    }

    function addMessage(sender, text) {
        const div = document.createElement("div");
        div.className = sender === "You" ? "user-msg" : "bot-msg";
        div.innerText = text;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showTyping() {
        const typingDiv = document.createElement("div");
        typingDiv.className = "typing";
        typingDiv.id = "typingIndicator";
        typingDiv.innerHTML = `
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
        `;
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function removeTyping() {
        const typing = document.getElementById("typingIndicator");
        if (typing) typing.remove();
    }

    function getBotResponse(msg) {
        msg = msg.toLowerCase();

        if (msg.includes("bca")) {
            return "BCA is a great IT course focusing on programming, software development and databases.";
        }
        if (msg.includes("btech")) {
            return "BTech is an engineering degree. Popular branches include CSE, Mechanical, Civil.";
        }
        if (msg.includes("mbbs")) {
            return "MBBS is a medical degree to become a doctor.";
        }
        if (msg.includes("design")) {
            return "You can explore BDes, UI/UX Design or Graphic Design courses.";
        }

        return "Tell me your interest (IT, Medical, Commerce, Design) and I will guide you 😊";
    }

});

