document.addEventListener("DOMContentLoaded", () => {
    initializeMatrix();
    initializeDraggableLogin();
    initializeThreatAlerts();
    initializeSystemMonitor();
    initializeTerminalFeed();
});

/* ==========================================
   MATRIX RAIN
========================================== */

function initializeMatrix() {
    const canvas = document.getElementById("matrix");

    if (!canvas) {
        return;
    }

    const ctx = canvas.getContext("2d");

    resizeCanvas();

    const characters =
        "01ABCDEFGHIJKLMNOPQRSTUVWXYZ#$%&@";

    const fontSize = 14;

    let columns =
        Math.floor(canvas.width / fontSize);

    let drops =
        Array(columns).fill(1);

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    function drawMatrix() {

        ctx.fillStyle =
            "rgba(11,18,32,0.08)";

        ctx.fillRect(
            0,
            0,
            canvas.width,
            canvas.height
        );

        ctx.fillStyle = "#00e5ff";

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
                drops[i] * fontSize
            );

            if (
                drops[i] * fontSize >
                canvas.height &&
                Math.random() > 0.975
            ) {
                drops[i] = 0;
            }

            drops[i]++;
        }
    }

    setInterval(
        drawMatrix,
        35
    );

    window.addEventListener(
        "resize",
        () => {

            resizeCanvas();

            columns =
                Math.floor(
                    canvas.width /
                    fontSize
                );

            drops =
                Array(columns).fill(1);

        }
    );
}

/* ==========================================
   DRAGGABLE LOGIN
========================================== */

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

            card.style.left =
                event.clientX -
                offsetX +
                "px";

            card.style.top =
                event.clientY -
                offsetY +
                "px";
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

/* ==========================================
   THREAT ALERTS
========================================== */

function initializeThreatAlerts() {

    const panel =
        document.querySelector(
            ".threat-panel"
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
        "MALICIOUS SESSION CREATED"
    ];

    const paragraph =
        panel.querySelector("p");

    setInterval(() => {

        const randomAlert =
            alerts[
                Math.floor(
                    Math.random() *
                    alerts.length
                )
            ];

        if (paragraph) {
            paragraph.textContent =
                randomAlert;
        }

    }, 5000);
}

/* ==========================================
   TERMINAL FEED
========================================== */

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

        const entry =
            document.createElement(
                "div"
            );

        entry.textContent =
            logs[
                Math.floor(
                    Math.random() *
                    logs.length
                )
            ];

        terminal.prepend(entry);

        while (
            terminal.children.length > 8
        ) {
            terminal.removeChild(
                terminal.lastChild
            );
        }

    }, 3000);
}

/* ==========================================
   SYSTEM MONITOR
========================================== */

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
                value + "%";

        });

    }, 2500);
}