let attackChart = null;

let chartRefreshInterval = null;

document.addEventListener(
    "DOMContentLoaded",
    () => {

        initializeCharts();

    }
);

/* ==================================================
   INIT
================================================== */

function initializeCharts() {

    loadAttackChart();

    startChartRefresh();

}

/* ==================================================
   AUTO REFRESH
================================================== */

function startChartRefresh() {

    if (chartRefreshInterval) {

        clearInterval(
            chartRefreshInterval
        );

    }

    chartRefreshInterval =
        setInterval(
            () => {

                if (
                    !document.hidden
                ) {

                    loadAttackChart();

                }

            },
            30000
        );

}

/* ==================================================
   LOAD DATA
================================================== */

async function loadAttackChart() {

    const canvas =
        document.getElementById(
            "attackChart"
        );

    if (!canvas) {
        return;
    }

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

        if (
            !response.ok
        ) {

            throw new Error(
                "Failed to load stats"
            );

        }

        const data =
            await response.json();

        const grouped =
            groupAttacksByHour(
                data.recent_attacks || []
            );

        renderAttackChart(
            canvas,
            grouped.labels,
            grouped.values
        );

    }

    catch (error) {

        console.error(
            "Chart error:",
            error
        );

    }

}

/* ==================================================
   GROUP ATTACKS
================================================== */

function groupAttacksByHour(
    attacks
) {

    const counter = {};

    attacks.forEach(
        attack => {

            if (
                !attack.timestamp
            ) {

                return;

            }

            const date =
                new Date(
                    attack.timestamp
                );

            if (
                Number.isNaN(
                    date.getTime()
                )
            ) {

                return;

            }

            const hour =
                date
                .getHours()
                .toString()
                .padStart(
                    2,
                    "0"
                );

            counter[hour] =
                (
                    counter[hour] || 0
                ) + 1;

        }
    );

    const labels = [];
    const values = [];

    for (
        let i = 0;
        i < 24;
        i++
    ) {

        const hour =
            i
            .toString()
            .padStart(
                2,
                "0"
            );

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

/* ==================================================
   CHART
================================================== */

function renderAttackChart(
    canvas,
    labels,
    values
) {

    const ctx =
        canvas.getContext(
            "2d"
        );

    const gradient =
        ctx.createLinearGradient(
            0,
            0,
            0,
            400
        );

    gradient.addColorStop(
        0,
        "rgba(0,229,255,.35)"
    );

    gradient.addColorStop(
        1,
        "rgba(0,229,255,0)"
    );

    if (
        attackChart
    ) {

        attackChart.data.labels =
            labels;

        attackChart.data.datasets[0].data =
            values;

        attackChart.update();

        return;

    }

    attackChart =
        new Chart(
            ctx,
            {

                type:
                    "line",

                data: {

                    labels,

                    datasets: [

                        {

                            label:
                                "Attack Attempts",

                            data:
                                values,

                            borderColor:
                                "#00e5ff",

                            backgroundColor:
                                gradient,

                            fill: true,

                            tension:
                                0.35,

                            borderWidth:
                                3,

                            pointRadius:
                                3,

                            pointHoverRadius:
                                6,

                            pointBackgroundColor:
                                "#00e5ff",

                            pointBorderColor:
                                "#ffffff",

                            pointBorderWidth:
                                1

                        }

                    ]

                },

                options: {

                    responsive:
                        true,

                    maintainAspectRatio:
                        false,

                    animation: {

                        duration:
                            800

                    },

                    interaction: {

                        mode:
                            "index",

                        intersect:
                            false

                    },

                    plugins: {

                        legend: {

                            labels: {

                                color:
                                    "#ffffff"

                            }

                        },

                        tooltip: {

                            backgroundColor:
                                "#08111f",

                            titleColor:
                                "#00e5ff",

                            bodyColor:
                                "#ffffff",

                            borderColor:
                                "#00e5ff",

                            borderWidth:
                                1

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

                                display:
                                    true,

                                text:
                                    "Hour",

                                color:
                                    "#00e5ff"

                            }

                        },

                        y: {

                            beginAtZero:
                                true,

                            grid: {

                                color:
                                    "rgba(255,255,255,.05)"

                            },

                            ticks: {

                                precision:
                                    0,

                                color:
                                    "#94a3b8"

                            },

                            title: {

                                display:
                                    true,

                                text:
                                    "Attack Count",

                                color:
                                    "#00e5ff"

                            }

                        }

                    }

                }

            }
        );

}

/* ==================================================
   VISIBILITY
================================================== */

document.addEventListener(
    "visibilitychange",
    () => {

        if (
            !document.hidden
        ) {

            loadAttackChart();

        }

    }
);