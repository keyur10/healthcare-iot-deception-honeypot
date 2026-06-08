document.addEventListener("DOMContentLoaded", () => {

    initializeAttackCounter();
    initializeDeviceCounter();
    initializeThreatLevel();
    initializeTrafficCounter();
    initializeTerminalFeed();
    initializeClock();
    initializeWidgetPulse();

});

/* ==================================================
   ATTACK COUNTER
================================================== */

function initializeAttackCounter() {

    const attackCounter =
        document.getElementById(
            "attackCounter"
        );

    if (!attackCounter) return;

    setInterval(() => {

        attackCounter.innerText =
            Math.floor(
                10 + Math.random() * 40
            );

    }, 2500);

}

/* ==================================================
   DEVICE COUNTER
================================================== */

function initializeDeviceCounter() {

    const deviceCounter =
        document.getElementById(
            "deviceCounter"
        );

    if (!deviceCounter) return;

    setInterval(() => {

        deviceCounter.innerText =
            Math.floor(
                85 + Math.random() * 25
            );

    }, 4000);

}

/* ==================================================
   THREAT LEVEL
================================================== */

function initializeThreatLevel() {

    const threatElement =
        document.querySelector(
            ".status-orange"
        );

    if (!threatElement) return;

    const levels = [

        {
            text: "LOW",
            color: "#00ff88"
        },

        {
            text: "MEDIUM",
            color: "#ff9f1a"
        },

        {
            text: "HIGH",
            color: "#ff304f"
        }

    ];

    setInterval(() => {

        const randomLevel =
            levels[
                Math.floor(
                    Math.random() *
                    levels.length
                )
            ];

        threatElement.innerText =
            randomLevel.text;

        threatElement.style.color =
            randomLevel.color;

    }, 6000);

}

/* ==================================================
   NETWORK TRAFFIC
================================================== */

function initializeTrafficCounter() {

    const trafficElement =
        document.querySelector(
            ".traffic-value"
        );

    if (!trafficElement) return;

    setInterval(() => {

        const value =
            (
                1 +
                Math.random() * 5
            ).toFixed(2);

        trafficElement.innerText =
            `${value} GB/s`;

    }, 3000);

}

/* ==================================================
   TERMINAL FEED
================================================== */

function initializeTerminalFeed() {

    const terminal =
        document.getElementById(
            "terminalFeed"
        );

    if (!terminal) return;

    const logs = [

        "[INFO] Healthcare Node Registered",

        "[INFO] MQTT Reconnaissance Detected",

        "[WARNING] SSH Brute Force Attempt",

        "[INFO] Smart Bed Connected",

        "[INFO] Patient Monitor Online",

        "[ALERT] Unauthorized Device Scan",

        "[INFO] Modbus Probe Captured",

        "[ALERT] Honeypot Triggered",

        "[INFO] Ventilator Telemetry Active",

        "[WARNING] Suspicious DNS Request",

        "[INFO] Threat Intelligence Updated",

        "[INFO] Fake Device Interaction Logged",

        "[ALERT] Malware Signature Matched",

        "[INFO] Infusion Pump Responded",

        "[INFO] Nurse Station Connected"

    ];

    setInterval(() => {

        const log =

            logs[
                Math.floor(
                    Math.random() *
                    logs.length
                )
            ];

        const timestamp =
            new Date()
            .toLocaleTimeString();

        const line =

            `<div>[${timestamp}] ${log}</div>`;

        terminal.innerHTML =
            line +
            terminal.innerHTML;

        const lines =
            terminal.querySelectorAll(
                "div"
            );

        if (
            lines.length > 12
        ) {

            lines[
                lines.length - 1
            ].remove();

        }

    }, 2000);

}

/* ==================================================
   LIVE CLOCK
================================================== */

function initializeClock() {

    const clock =
        document.getElementById(
            "liveClock"
        );

    if (!clock) return;

    setInterval(() => {

        clock.innerText =
            new Date()
            .toLocaleString();

    }, 1000);

}

/* ==================================================
   PANEL GLOW EFFECT
================================================== */

function initializeWidgetPulse() {

    const cards =
        document.querySelectorAll(
            ".widget-card"
        );

    setInterval(() => {

        cards.forEach(card => {

            card.style.boxShadow =
                `0 0 ${
                    15 +
                    Math.random() * 25
                }px rgba(0,217,255,.15)`;

        });

    }, 2500);

}

/* ==================================================
   RANDOM ATTACK TYPES
================================================== */

setInterval(() => {

    const attacks =
        document.querySelectorAll(
            ".attack-list li"
        );

    attacks.forEach(item => {

        if (
            Math.random() > 0.7
        ) {

            item.style.color =
                "#ff304f";

            setTimeout(() => {

                item.style.color =
                    "#9fe8ff";

            }, 1000);

        }

    });

}, 3500);

/* ==================================================
   LOGIN CARD PARALLAX
================================================== */

document.addEventListener(
    "mousemove",
    event => {

        const card =
            document.querySelector(
                ".login-card"
            );

        if (!card) return;

        const x =
            (
                event.clientX /
                window.innerWidth
            ) - 0.5;

        const y =
            (
                event.clientY /
                window.innerHeight
            ) - 0.5;

        card.style.transform =

            `translateY(-5px)
             rotateY(${x * 4}deg)
             rotateX(${y * -4}deg)`;

    }
);

/* ==================================================
   SYSTEM STATUS BLINK
================================================== */

setInterval(() => {

    const greenStatus =
        document.querySelector(
            ".status-green"
        );

    if (!greenStatus) return;

    greenStatus.style.opacity =
        greenStatus.style.opacity ===
        "0.6"
            ? "1"
            : "0.6";

}, 1500);

/* ==================================================
   FAKE LIVE ALERTS
================================================== */

const alertMessages = [

    "Suspicious MQTT Scan",
    "Brute Force Attempt",
    "Unknown IoT Device",
    "Medical Network Probe",
    "Unauthorized Access",
    "Malware Beacon",
    "Smart Bed Enumeration"

];

setInterval(() => {

    console.log(

        "[SOC ALERT]",

        alertMessages[
            Math.floor(
                Math.random() *
                alertMessages.length
            )
        ]

    );

}, 5000);