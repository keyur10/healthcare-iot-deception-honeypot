// static/js/realtime.js

document.addEventListener(
    "DOMContentLoaded",
    () => {

        updateDashboard();

        setInterval(
            updateDashboard,
            10000
        );

    }
);

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

        updateStatistics(data);

        updateAttackFeed(data);

        updateAttackTable(data);

        updateThreatLevel(data);

    }

    catch (error) {

        console.error(
            "Realtime update error:",
            error
        );

    }

}

function updateStatistics(data) {

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
            data.total_attacks;

    }

    if (uniqueIps) {

        uniqueIps.textContent =
            data.unique_ips;

    }

}

function updateThreatLevel(data) {

    const threat =
        document.getElementById(
            "threat-level"
        );

    if (!threat) {
        return;
    }

    threat.textContent =
        data.threat_level;

}

function updateAttackFeed(data) {

    const container =
        document.getElementById(
            "attack-feed"
        );

    if (!container) {
        return;
    }

    const attacks =
        data.recent_attacks || [];

    container.innerHTML = "";

    attacks.forEach(attack => {

        container.innerHTML += `

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

        `;

    });

}

function updateAttackTable(data) {

    const table =
        document.querySelector(
            "#attackTable tbody"
        );

    if (!table) {
        return;
    }

    const attacks =
        data.recent_attacks || [];

    table.innerHTML = "";

    attacks.forEach(attack => {

        table.innerHTML += `

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

        `;

    });

}