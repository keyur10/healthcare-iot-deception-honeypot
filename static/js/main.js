/* =====================================================
   HIDHN SOC PLATFORM
   Main JavaScript
===================================================== */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        initializeClock();

        initializeNotifications();

        initializeSearch();

        initializeLoadingOverlay();

        initializeFlashMessages();

        initializeCardEffects();

        initializeSidebarHighlight();

    }
);

/* =====================================================
   LIVE CLOCK
===================================================== */

function initializeClock() {

    const clock =
        document.getElementById(
            "live-clock"
        );

    if (!clock) return;

    function updateClock() {

        const now =
            new Date();

        clock.textContent =
            now.toLocaleTimeString(
                "en-US",
                {
                    hour12: true
                }
            );

    }

    updateClock();

    setInterval(
        updateClock,
        1000
    );

}

/* =====================================================
   NOTIFICATIONS
===================================================== */

function initializeNotifications() {

    const btn =
        document.getElementById(
            "notificationBtn"
        );

    const dropdown =
        document.getElementById(
            "notificationDropdown"
        );

    if (!btn || !dropdown)
        return;

    btn.addEventListener(
        "click",
        function (e) {

            e.stopPropagation();

            dropdown.classList.toggle(
                "show"
            );

        }
    );

    document.addEventListener(
        "click",
        function () {

            dropdown.classList.remove(
                "show"
            );

        }
    );

}

/* =====================================================
   GLOBAL SEARCH
===================================================== */

function initializeSearch() {

    const search =
        document.getElementById(
            "globalSearch"
        );

    if (!search)
        return;

    search.addEventListener(
        "keyup",
        function (e) {

            if (
                e.key === "Enter"
            ) {

                const query =
                    this.value
                    .trim();

                if (
                    query.length > 0
                ) {

                    console.log(
                        "Search:",
                        query
                    );

                }

            }

        }
    );

}

/* =====================================================
   LOADING OVERLAY
===================================================== */

function initializeLoadingOverlay() {

    const loader =
        document.getElementById(
            "loading-overlay"
        );

    if (!loader)
        return;

    setTimeout(
        function () {

            loader.style.opacity =
                "0";

            setTimeout(
                function () {

                    loader.style.display =
                        "none";

                },
                500
            );

        },
        600
    );

}

/* =====================================================
   FLASH MESSAGES
===================================================== */

function initializeFlashMessages() {

    const messages =
        document.querySelectorAll(
            ".flash-message"
        );

    if (
        messages.length === 0
    )
        return;

    messages.forEach(
        function (
            message
        ) {

            setTimeout(
                function () {

                    message.style.opacity =
                        "0";

                    message.style.transform =
                        "translateX(50px)";

                    setTimeout(
                        function () {

                            message.remove();

                        },
                        500
                    );

                },
                4000
            );

        }
    );

}

/* =====================================================
   CARD HOVER EFFECTS
===================================================== */

function initializeCardEffects() {

    const cards =
        document.querySelectorAll(
            ".stat-card, .widget-card, .report-card, .geo-card"
        );

    cards.forEach(
        function (
            card
        ) {

            card.addEventListener(
                "mouseenter",
                function () {

                    this.style.transform =
                        "translateY(-4px)";

                }
            );

            card.addEventListener(
                "mouseleave",
                function () {

                    this.style.transform =
                        "translateY(0px)";

                }
            );

        }
    );

}

/* =====================================================
   ACTIVE SIDEBAR
===================================================== */

function initializeSidebarHighlight() {

    const links =
        document.querySelectorAll(
            ".sidebar-nav a"
        );

    const current =
        window.location.pathname;

    links.forEach(
        function (
            link
        ) {

            const href =
                link.getAttribute(
                    "href"
                );

            if (
                href === current
            ) {

                link.classList.add(
                    "active"
                );

            }

        }
    );

}

/* =====================================================
   DASHBOARD COUNTERS
===================================================== */

function animateCounter(
    elementId,
    target
) {

    const element =
        document.getElementById(
            elementId
        );

    if (!element)
        return;

    let current = 0;

    const increment =
        target / 50;

    const timer =
        setInterval(
            function () {

                current +=
                    increment;

                if (
                    current >=
                    target
                ) {

                    current =
                        target;

                    clearInterval(
                        timer
                    );

                }

                element.textContent =
                    Math.floor(
                        current
                    );

            },
            30
        );

}

/* =====================================================
   OPTIONAL DASHBOARD
===================================================== */

animateCounter(
    "attackCounter",
    12
);

animateCounter(
    "deviceCounter",
    98
);

animateCounter(
    "honeypotCount",
    24
);