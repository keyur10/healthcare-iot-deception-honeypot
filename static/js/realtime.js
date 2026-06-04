document.addEventListener(
    "DOMContentLoaded",
    () => {

        initializeRealtime();

    }
);

/* ==================================================
   REALTIME INIT
================================================== */

let previousAttackCount = 0;

function initializeRealtime() {

    initializeClock();

    initializeConnectionStatus();

    initializeRealtimeMonitor();

}

/* ==================================================
   CLOCK
================================================== */

function initializeClock() {

    const clock =
        document.getElementById(
            "soc-clock"
        );

    if (!clock) {
        return;
    }

    function updateClock() {

        clock.textContent =
            new Date()
            .toLocaleString();

    }

    updateClock();

    setInterval(
        updateClock,
        1000
    );

}

/* ==================================================
   CONNECTION STATUS
================================================== */

function initializeConnectionStatus() {

    const indicator =
        document.getElementById(
            "connection-status"
        );

    if (!indicator) {
        return;
    }

    function updateStatus() {

        if (
            navigator.onLine
        ) {

            indicator.textContent =
                "ONLINE";

            indicator.className =
                "badge bg-success";

        }

        else {

            indicator.textContent =
                "OFFLINE";

            indicator.className =
                "badge bg-danger";

        }

    }

    updateStatus();

    window.addEventListener(
        "online",
        updateStatus
    );

    window.addEventListener(
        "offline",
        updateStatus
    );

}

/* ==================================================
   REALTIME MONITOR
================================================== */

async function checkForNewAttacks() {

    try {

        const response =
            await fetch(
                "/api/stats"
            );

        if (!response.ok) {

            console.error(
                "API Error:",
                response.status
            );

            return;

        }

        const contentType =
            response.headers.get(
                "content-type"
            );

        if (
            !contentType ||
            !contentType.includes(
                "application/json"
            )
        ) {

            console.error(
                "API returned HTML instead of JSON"
            );

            return;

        }

        const data =
            await response.json();

        const total =
            data.total_attacks || 0;

        if (
            previousAttackCount !== 0 &&
            total > previousAttackCount
        ) {

            const newAttacks =
                total -
                previousAttackCount;

            showNotification(
                `${newAttacks} New Attack(s) Detected`
            );

        }

        previousAttackCount =
            total;

        updateLastRefresh();

    }

    catch (error) {

        console.error(
            "Realtime monitor failed:",
            error
        );

    }

}
/* ==================================================
   LAST REFRESH
================================================== */

function updateLastRefresh() {

    const refresh =
        document.getElementById(
            "last-refresh"
        );

    if (!refresh) {
        return;
    }

    refresh.textContent =
        new Date()
        .toLocaleTimeString();

}

/* ==================================================
   NOTIFICATIONS
================================================== */

function showNotification(
    message
) {

    const container =
        document.getElementById(
            "notification-container"
        );

    if (!container) {
        return;
    }

    const notification =
        document.createElement(
            "div"
        );

    notification.className =
        "alert alert-warning shadow";

    notification.innerHTML = `

        <i class="fas fa-bell me-2"></i>

        ${message}

    `;

    container.prepend(
        notification
    );

    setTimeout(
        () => {

            notification.remove();

        },
        5000
    );

}

/* ==================================================
   PAGE VISIBILITY
================================================== */

document.addEventListener(
    "visibilitychange",
    () => {

        if (
            !document.hidden
        ) {

            updateLastRefresh();

        }

    }
);