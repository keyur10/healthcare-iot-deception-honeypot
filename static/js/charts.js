let attackChart = null;

document.addEventListener("DOMContentLoaded", async () => {
    await loadAttackChart();
});

async function loadAttackChart() {

    const canvas =
        document.getElementById("attackChart");

    if (!canvas) {
        return;
    }

    try {

        const response =
            await fetch("/api/stats");

        const data =
            await response.json();

        const attacks =
            data.recent_attacks || [];

        const grouped =
            groupAttacksByHour(attacks);

        createAttackChart(
            canvas,
            grouped.labels,
            grouped.values
        );

    } catch (error) {

        console.error(
            "Chart error:",
            error
        );

    }

}

function groupAttacksByHour(attacks) {

    const counter = {};

    attacks.forEach(attack => {

        if (!attack.timestamp) {
            return;
        }

        const date =
            new Date(
                attack.timestamp
            );

        const hour =
            date.getHours()
                .toString()
                .padStart(2, "0");

        counter[hour] =
            (counter[hour] || 0) + 1;

    });

    const labels = [];
    const values = [];

    for (let i = 0; i < 24; i++) {

        const hour =
            i.toString()
             .padStart(2, "0");

        labels.push(
            `${hour}:00`
        );

        values.push(
            counter[hour] || 0
        );

    }

    return {
        labels,
        values,
    };

}

function createAttackChart(
    canvas,
    labels,
    values
) {

    if (attackChart) {
        attackChart.destroy();
    }

    attackChart = new Chart(canvas, {

        type: "line",

        data: {

            labels,

            datasets: [

                {

                    label:
                        "Attack Attempts",

                    data: values,

                    borderColor:
                        "#00e5ff",

                    backgroundColor:
                        "rgba(0,229,255,.15)",

                    fill: true,

                    borderWidth: 2,

                    tension: 0.3,

                    pointRadius: 4,

                    pointHoverRadius: 6,

                    pointBackgroundColor:
                        "#00e5ff",

                    pointBorderColor:
                        "#ffffff",

                    pointBorderWidth: 1

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            animation: {
                duration: 1000
            },

            interaction: {
                intersect: false,
                mode: "index"
            },

            plugins: {

                legend: {

                    labels: {
                        color:
                            "#f8fafc"
                    }

                },

                tooltip: {

                    backgroundColor:
                        "#111827",

                    titleColor:
                        "#00e5ff",

                    bodyColor:
                        "#f8fafc",

                    borderColor:
                        "#00e5ff",

                    borderWidth: 1

                }

            },

            scales: {

                x: {

                    grid: {

                        color:
                            "rgba(255,255,255,.05)"

                    },

                    ticks: {

                        color:
                            "#94a3b8"

                    },

                    title: {

                        display: true,

                        text:
                            "Hour",

                        color:
                            "#00e5ff"

                    }

                },

                y: {

                    beginAtZero: true,

                    grid: {

                        color:
                            "rgba(255,255,255,.05)"

                    },

                    ticks: {

                        color:
                            "#94a3b8"

                    },

                    title: {

                        display: true,

                        text:
                            "Attack Count",

                        color:
                            "#00e5ff"

                    }

                }

            }

        }

    });

}

setInterval(
    loadAttackChart,
    30000
);