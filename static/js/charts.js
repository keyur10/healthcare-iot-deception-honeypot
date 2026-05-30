document.addEventListener("DOMContentLoaded", () => {
    createAttackChart();
});

let attackChart = null;

function createAttackChart() {
    const canvas = document.getElementById("attackChart");

    if (!canvas) {
        return;
    }

    if (attackChart) {
        attackChart.destroy();
    }

    attackChart = new Chart(canvas, {
        type: "line",

        data: {
            labels: [
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri",
                "Sat",
                "Sun"
            ],

            datasets: [
                {
                    label: "Attack Attempts",

                    data: [12, 19, 8, 15, 24, 18, 30],

                    borderColor: "#00e5ff",

                    backgroundColor:
                        "rgba(0, 229, 255, 0.15)",

                    borderWidth: 2,

                    fill: true,

                    tension: 0,

                    pointRadius: 4,

                    pointHoverRadius: 6,

                    pointBackgroundColor: "#00e5ff",

                    pointBorderColor: "#ffffff",

                    pointBorderWidth: 1
                }
            ]
        },

        options: {
            responsive: true,

            maintainAspectRatio: false,

            animation: false,

            resizeDelay: 100,

            interaction: {
                intersect: false,
                mode: "index"
            },

            plugins: {
                legend: {
                    display: true,

                    labels: {
                        color: "#f8fafc"
                    }
                },

                tooltip: {
                    enabled: true,

                    backgroundColor: "#111827",

                    titleColor: "#00e5ff",

                    bodyColor: "#f8fafc",

                    borderColor: "#00e5ff",

                    borderWidth: 1
                }
            },

            scales: {

                x: {
                    grid: {
                        color: "rgba(255,255,255,0.05)"
                    },

                    ticks: {
                        color: "#94a3b8"
                    },

                    title: {
                        display: true,
                        text: "Day",
                        color: "#00e5ff"
                    }
                },

                y: {
                    beginAtZero: true,

                    grid: {
                        color: "rgba(255,255,255,0.05)"
                    },

                    ticks: {
                        color: "#94a3b8"
                    },

                    title: {
                        display: true,
                        text: "Attack Count",
                        color: "#00e5ff"
                    }
                }
            }
        }
    });
}