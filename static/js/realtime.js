document.addEventListener("DOMContentLoaded", () => {
    startRealtimeUpdates();
});

function startRealtimeUpdates() {
    setInterval(async () => {
        try {
            const response = await fetch("/api/stats");

            if (!response.ok) {
                return;
            }

            const data = await response.json();

            console.log("Realtime update:", data);

            updateStatistics(data);

        } catch (error) {
            console.error(error);
        }

    }, 10000);
}

function updateStatistics(data) {
    const totalAttacks = document.getElementById("total-attacks");
    const uniqueIps = document.getElementById("unique-ips");

    if (totalAttacks) {
        totalAttacks.textContent = data.total_attacks;
    }

    if (uniqueIps) {
        uniqueIps.textContent = data.unique_ips;
    }
}