document.addEventListener("DOMContentLoaded", () => {
    initializeDashboard();
    startAutoRefresh();
});

function initializeDashboard() {
    console.log("Dashboard loaded");
}

function startAutoRefresh() {
    setInterval(async () => {
        try {
            const response = await fetch("/api/stats");

            if (!response.ok) {
                return;
            }

            const data = await response.json();

            updateCounters(data);
        } catch (error) {
            console.error("Refresh failed:", error);
        }
    }, 10000);
}

function updateCounters(data) {
    console.log("Latest stats:", data);
}