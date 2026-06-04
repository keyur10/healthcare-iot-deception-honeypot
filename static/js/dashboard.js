document.addEventListener(
    "DOMContentLoaded",
    () => {

        initializeDashboard();

    }
);

/* ==================================================
   DASHBOARD INIT
================================================== */

let refreshInterval = null;

function initializeDashboard() {

    console.log(
        "Hybrid SOC Dashboard Initialized"
    );

    updateDashboard();

    startAutoRefresh();

}

/* ==================================================
   AUTO REFRESH
================================================== */

function startAutoRefresh() {

    if (refreshInterval) {

        clearInterval(
            refreshInterval
        );

    }

    refreshInterval =
        setInterval(
            updateDashboard,
            10000
        );

}

/* ==================================================
   FETCH DASHBOARD DATA
================================================== */

async function updateDashboard() {

    try {

        const controller =
            new AbortController();

        const timeout =
            setTimeout(
                () =>
                    controller.abort(),
                5000
            );

        const response =
            await fetch(
                "/api/stats",
                {
                    signal:
                        controller.signal
                }
            );

        clearTimeout(
            timeout
        );

        if (!response.ok) {

            throw new Error(
                "API Error"
            );

        }

        const data =
            await response.json();

        updateCounters(data);

        updateThreatLevel(data);

        updateAttackFeed(data);

        updateAttackTable(data);

        updateLastRefresh();

    }

    catch (error) {

        console.error(
            "Dashboard refresh failed:",
            error
        );

    }

}

/* ==================================================
   COUNTERS
================================================== */

function animateCounter(
    element,
    target
) {

    if (!element) {
        return;
    }

    const start =
        Number(
            element.textContent
        ) || 0;

    const duration = 1000;

    const startTime =
        performance.now();

    function update(
        currentTime
    ) {

        const progress =
            Math.min(
                (
                    currentTime -
                    startTime
                ) /
                duration,
                1
            );

        const value =
            Math.floor(
                start +
                (
                    target -
                    start
                ) *
                progress
            );

        element.textContent =
            value;

        if (
            progress < 1
        ) {

            requestAnimationFrame(
                update
            );

        }

    }

    requestAnimationFrame(
        update
    );

}

function updateCounters(
    data
) {

    animateCounter(
        document.getElementById(
            "total-attacks"
        ),
        data.total_attacks || 0
    );

    animateCounter(
        document.getElementById(
            "unique-ips"
        ),
        data.unique_ips || 0
    );

}

/* ==================================================
   THREAT LEVEL
================================================== */

function updateThreatLevel(
    data
) {

    const element =
        document.getElementById(
            "threat-level"
        );

    if (!element) {
        return;
    }

    element.textContent =
        data.threat_level ||
        "LOW";

    element.className =
        "threat-badge";

    switch (
        data.threat_level
    ) {

        case "CRITICAL":

            element.classList.add(
                "bg-danger"
            );

            break;

        case "HIGH":

            element.classList.add(
                "bg-warning"
            );

            break;

        case "MEDIUM":

            element.classList.add(
                "bg-info"
            );

            break;

        default:

            element.classList.add(
                "bg-success"
            );

    }

}

/* ==================================================
   ATTACK FEED
================================================== */

function updateAttackFeed(
    data
) {

    const feed =
        document.getElementById(
            "attack-feed"
        );

    if (!feed) {
        return;
    }

    const attacks =
        data.recent_attacks ||
        [];

    feed.innerHTML = "";

    attacks.forEach(
        attack => {

            const item =
                document.createElement(
                    "div"
                );

            item.className =
                "feed-item";

            item.innerHTML = `
                <div class="feed-time">
                    ${attack.timestamp}
                </div>

                <div class="fw-bold text-info">
                    ${attack.ip}
                </div>

                <small>
                    Username:
                    ${attack.username}
                </small>

                <br>

                <small>
                    Password:
                    ${attack.password}
                </small>
            `;

            feed.appendChild(
                item
            );

        }
    );

}

/* ==================================================
   ATTACK TABLE
================================================== */

function updateAttackTable(
    data
) {

    const tbody =
        document.querySelector(
            "#attackTable tbody"
        );

    if (!tbody) {
        return;
    }

    tbody.innerHTML = "";

    (
        data.recent_attacks ||
        []
    ).forEach(
        attack => {

            const row =
                document.createElement(
                    "tr"
                );

            row.innerHTML = `
                <td>${attack.ip}</td>
                <td>${attack.username}</td>
                <td>${attack.password}</td>
                <td>${attack.timestamp}</td>
            `;

            tbody.appendChild(
                row
            );

        }
    );

}

/* ==================================================
   LAST REFRESH
================================================== */

function updateLastRefresh() {

    const element =
        document.getElementById(
            "last-refresh"
        );

    if (!element) {
        return;
    }

    element.textContent =
        new Date()
        .toLocaleTimeString();

}

/* ==================================================
   PAGE VISIBILITY
================================================== */

document.addEventListener(
    "visibilitychange",
    () => {

        if (
            document.hidden
        ) {

            clearInterval(
                refreshInterval
            );

        }

        else {

            startAutoRefresh();

            updateDashboard();

        }

    }
);