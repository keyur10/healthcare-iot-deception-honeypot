// static/js/dashboard.js

document.addEventListener(
    "DOMContentLoaded",
    () => {

        initializeDashboard();

        startAutoRefresh();

    }
);

function initializeDashboard() {

    console.log(
        "SOC Dashboard Initialized"
    );

}

function startAutoRefresh() {

    updateDashboard();

    setInterval(
        updateDashboard,
        10000
    );

}

async function updateDashboard() {

    try {

        const response =
            await fetch(
                "/api/stats"
            );

        if (!response.ok) {
            return;
        }

        const data =
            await response.json();

        updateCounters(data);

        updateThreatLevel(data);

        updateAttackFeed(data);

        updateAttackTable(data);

    }

    catch (error) {

        console.error(
            "Refresh failed:",
            error
        );

    }

}

function updateCounters(data) {

    const totalAttacks =
        document.getElementById(
            "total-attacks"
        );

    const uniqueIps =
        document.getElementById(
            "unique-ips"
        );

    if (totalAttacks) {

        totalAttacks.textContent =
            data.total_attacks ?? 0;

    }

    if (uniqueIps) {

        uniqueIps.textContent =
            data.unique_ips ?? 0;

    }

}

function updateThreatLevel(data) {

    const threatElement =
        document.getElementById(
            "threat-level"
        );

    if (!threatElement) {
        return;
    }

    threatElement.textContent =
        data.threat_level ?? "LOW";

    threatElement.className = "";

    switch (data.threat_level) {

        case "CRITICAL":

            threatElement.classList.add(
                "text-danger"
            );

            break;

        case "HIGH":

            threatElement.classList.add(
                "text-warning"
            );

            break;

        case "MEDIUM":

            threatElement.classList.add(
                "text-info"
            );

            break;

        default:

            threatElement.classList.add(
                "text-success"
            );

    }

}

function updateAttackFeed(data) {

    const feed =
        document.getElementById(
            "attack-feed"
        );

    if (!feed) {
        return;
    }

    const attacks =
        data.recent_attacks || [];

    feed.innerHTML = "";

    attacks.forEach(attack => {

        feed.insertAdjacentHTML(
            "beforeend",

            `
            <div class="feed-item">

                <div class="feed-time">
                    ${attack.timestamp}
                </div>

                <strong>
                    ${attack.ip}
                </strong>

                <br>

                Username:
                ${attack.username}

                <br>

                Password:
                ${attack.password}

            </div>
            `
        );

    });

}

function updateAttackTable(data) {

    const tbody =
        document.querySelector(
            "#attackTable tbody"
        );

    if (!tbody) {
        return;
    }

    const attacks =
        data.recent_attacks || [];

    tbody.innerHTML = "";

    attacks.forEach(attack => {

        tbody.insertAdjacentHTML(
            "beforeend",

            `
            <tr>

                <td>
                    ${attack.ip}
                </td>

                <td>
                    ${attack.username}
                </td>

                <td>
                    ${attack.password}
                </td>

                <td>
                    ${attack.timestamp}
                </td>

            </tr>
            `
        );

    });

}