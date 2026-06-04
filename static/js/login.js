document.addEventListener("DOMContentLoaded", () => {

    initializeMatrix();

    initializeDraggableLogin();

    initializeThreatAlerts();

    initializeSystemMonitor();

    initializeTerminalFeed();

    initializeClock();

    initializeGeoIntel();
    
    initializeRoleMfa();
});

/* ==================================================
   MATRIX RAIN
================================================== */

function initializeMatrix() {

    const canvas =
        document.getElementById(
            "matrix"
        );

    if (!canvas) {
        return;
    }

    const ctx =
        canvas.getContext(
            "2d"
        );

    const characters =
        "01ABCDEFGHIJKLMNOPQRSTUVWXYZ#$%&@";

    const fontSize = 14;

    let columns;
    let drops;

    function resizeCanvas() {

        canvas.width =
            window.innerWidth;

        canvas.height =
            window.innerHeight;

        columns =
            Math.floor(
                canvas.width /
                fontSize
            );

        drops =
            Array(columns)
            .fill(1);

    }

    function drawMatrix() {

        ctx.fillStyle =
            "rgba(5,11,20,0.08)";

        ctx.fillRect(
            0,
            0,
            canvas.width,
            canvas.height
        );

        ctx.fillStyle =
            "#00e5ff";

        ctx.font =
            `${fontSize}px Consolas`;

        for (
            let i = 0;
            i < drops.length;
            i++
        ) {

            const char =
                characters[
                    Math.floor(
                        Math.random() *
                        characters.length
                    )
                ];

            ctx.fillText(
                char,
                i * fontSize,
                drops[i] *
                fontSize
            );

            if (
                drops[i] *
                    fontSize >
                canvas.height &&
                Math.random() >
                    0.975
            ) {

                drops[i] = 0;

            }

            drops[i]++;

        }

    }

    function animate() {

        drawMatrix();

        requestAnimationFrame(
            animate
        );

    }

    resizeCanvas();

    animate();

    window.addEventListener(
        "resize",
        resizeCanvas
    );

}

/* ==================================================
   DRAGGABLE LOGIN
================================================== */

function initializeDraggableLogin() {

    const card =
        document.getElementById(
            "draggable-login"
        );

    if (!card) {
        return;
    }

    let dragging = false;

    let offsetX = 0;
    let offsetY = 0;

    card.style.cursor =
        "grab";

    card.addEventListener(
        "mousedown",
        event => {

            dragging = true;

            offsetX =
                event.clientX -
                card.offsetLeft;

            offsetY =
                event.clientY -
                card.offsetTop;

            card.style.cursor =
                "grabbing";

        }
    );

    document.addEventListener(
        "mousemove",
        event => {

            if (!dragging) {
                return;
            }

            card.style.position =
                "absolute";

            const left =
                Math.max(
                    0,
                    Math.min(
                        window.innerWidth -
                        card.offsetWidth,
                        event.clientX -
                        offsetX
                    )
                );

            const top =
                Math.max(
                    0,
                    Math.min(
                        window.innerHeight -
                        card.offsetHeight,
                        event.clientY -
                        offsetY
                    )
                );

            card.style.left =
                `${left}px`;

            card.style.top =
                `${top}px`;

        }
    );

    document.addEventListener(
        "mouseup",
        () => {

            dragging = false;

            card.style.cursor =
                "grab";

        }
    );

}

/* ==================================================
   THREAT ALERTS
================================================== */

function initializeThreatAlerts() {

    const panel =
        document.querySelector(
            ".threat-panel p"
        );

    if (!panel) {
        return;
    }

    const alerts = [

        "SSH BRUTE FORCE DETECTED",

        "TELNET SCAN IDENTIFIED",

        "BOTNET ACTIVITY OBSERVED",

        "UNAUTHORIZED LOGIN ATTEMPT",

        "HIGH RISK SOURCE IP",

        "SUSPICIOUS CREDENTIAL SPRAY",

        "REMOTE ACCESS ATTEMPT",

        "MALICIOUS SESSION CREATED",

        "IOT DEVICE COMPROMISE",

        "THREAT LEVEL ELEVATED"

    ];

    setInterval(() => {

        panel.textContent =
            alerts[
                Math.floor(
                    Math.random() *
                    alerts.length
                )
            ];

    }, 5000);

}

/* ==================================================
   TERMINAL FEED
================================================== */

function initializeTerminalFeed() {

    const terminal =
        document.querySelector(
            ".terminal-feed"
        );

    if (!terminal) {
        return;
    }

    const logs = [

        "> SSH LOGIN FAILED",

        "> ROOT ACCESS ATTEMPT",

        "> BOTNET CONNECTION",

        "> SESSION OPENED",

        "> INVALID PASSWORD",

        "> ATTACK DETECTED",

        "> CREDENTIAL HARVESTING",

        "> CONNECTION CLOSED",

        "> PORT SCAN IDENTIFIED",

        "> MALICIOUS PAYLOAD BLOCKED"

    ];

    setInterval(() => {

        const line =
            document.createElement(
                "div"
            );

        const text =
            logs[
                Math.floor(
                    Math.random() *
                    logs.length
                )
            ];

        line.textContent =
            text;

        terminal.prepend(
            line
        );

        while (
            terminal.children
                .length > 8
        ) {

            terminal.removeChild(
                terminal.lastChild
            );

        }

    }, 2500);

}

/* ==================================================
   SYSTEM MONITOR
================================================== */

function initializeSystemMonitor() {

    const bars =
        document.querySelectorAll(
            ".progress-bar"
        );

    if (!bars.length) {
        return;
    }

    setInterval(() => {

        bars.forEach(bar => {

            const value =
                Math.floor(
                    Math.random() * 90
                ) + 10;

            bar.style.width =
                `${value}%`;

        });

    }, 2500);

}

/* ==================================================
   LIVE CLOCK
================================================== */

function initializeClock() {

    const clock =
        document.getElementById(
            "soc-live-clock"
        );

    if (!clock) {
        return;
    }

    setInterval(() => {

        clock.textContent =
            new Date()
            .toLocaleString();

    }, 1000);

}

/* ==================================================
   GEO INTELLIGENCE
================================================== */

function initializeGeoIntel() {

    const geo =
        document.getElementById(
            "geo-country"
        );

    if (!geo) {
        return;
    }

    const countries = [

        "United States",
        "Russia",
        "China",
        "Iran",
        "Germany",
        "India",
        "Brazil",
        "Unknown"

    ];

    setInterval(() => {

        geo.textContent =
            countries[
                Math.floor(
                    Math.random() *
                    countries.length
                )
            ];

    }, 4000);

}
/* ==================================================
   ROLE MFA CHECK
================================================== */

function initializeRoleMfa() {

    const usernameInput =
        document.getElementById(
            "username"
        );

    const mfaGroup =
        document.getElementById(
            "mfa-group"
        );

    if (
        !usernameInput ||
        !mfaGroup
    ) {

        return;

    }

    usernameInput.addEventListener(
        "blur",
        async () => {

            const username =
                usernameInput.value.trim();

            if (!username) {

                mfaGroup.style.display =
                    "none";

                return;

            }

            try {

                const response =
                    await fetch(
                        `/api/user-role/${username}`
                    );

                const data =
                    await response.json();

                if (
                    data.role === "admin"
                ) {

                    mfaGroup.style.display =
                        "none";

                }

                else if (
                    data.role === "analyst" ||
                    data.role === "user"
                ) {

                    mfaGroup.style.display =
                        "block";

                }

                else {

                    mfaGroup.style.display =
                        "none";

                }

            }

            catch {

                mfaGroup.style.display =
                    "none";

            }

        }
    );

}
const usernameInput =
    document.getElementById(
        "username"
    );

const mfaGroup =
    document.getElementById(
        "mfa-group"
    );

if (
    usernameInput &&
    mfaGroup
) {

    mfaGroup.style.display =
        "none";

    usernameInput.addEventListener(
        "blur",
        async () => {

            const username =
                usernameInput.value.trim();

            if (!username) {

                mfaGroup.style.display =
                    "none";

                return;

            }

            try {

                const response =
                    await fetch(
                        `/api/user-role/${username}`
                    );

                const data =
                    await response.json();

                if (
                    data.role &&
                    data.role.toLowerCase() !== "admin"
                ) {

                    mfaGroup.style.display =
                        "block";

                }

                else {

                    mfaGroup.style.display =
                        "none";

                }

            }

            catch {

                mfaGroup.style.display =
                    "none";

            }

        }
    );

}