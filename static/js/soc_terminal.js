const terminalInput =
    document.getElementById(
        "terminalInput"
    );

const terminalOutput =
    document.getElementById(
        "terminalOutput"
    );

document.addEventListener(
    "DOMContentLoaded",
    () => {

        initializeClock();

        initializeLiveEvents();

        terminalInput.focus();

    }
);

/* ==========================================
   CLOCK
========================================== */

function initializeClock() {

    const clock =
        document.getElementById(
            "terminalClock"
        );

    if (!clock) return;

    function updateClock() {

        clock.textContent =
            new Date()
            .toLocaleTimeString();

    }

    updateClock();

    setInterval(
        updateClock,
        1000
    );

}

/* ==========================================
   COMMAND INPUT
========================================== */

terminalInput.addEventListener(
    "keydown",
    async function(event) {

        if (
            event.key !== "Enter"
        ) {
            return;
        }

        const command =
            this.value.trim();

        if (!command) {
            return;
        }

        appendLine(
            `soc@hidhn:~$ ${command}`,
            "command-info"
        );

        this.value = "";

        if (
            command.toLowerCase() ===
            "clear"
        ) {

            clearTerminal();

            return;

        }

        try {

            const response =
                await fetch(
                    "/api/terminal",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                            "application/json"
                        },

                        body:
                        JSON.stringify({

                            command:
                                command

                        })
                    }
                );

            const data =
                await response.json();

            displayResult(
                data
            );

        }

        catch(error) {

            appendLine(
                "[ERROR] Backend Connection Failed",
                "command-error"
            );

            console.error(
                error
            );

        }

    }
);

/* ==========================================
   OUTPUT DISPLAY
========================================== */

function displayResult(
    data
) {

    if (
        !data.output
    ) {

        appendLine(
            "No Response",
            "command-warning"
        );

        return;

    }

    data.output.forEach(
        line => {

            appendLine(
                line,
                "command-output"
            );

        }
    );

}

function appendLine(
    text,
    className = ""
) {

    const div =
        document.createElement(
            "div"
        );

    div.className =
        className;

    div.textContent =
        text;

    terminalOutput.appendChild(
        div
    );

    terminalOutput.scrollTop =
        terminalOutput.scrollHeight;

}
/* ==========================================
   CLEAR TERMINAL
========================================== */

function clearTerminal() {

    terminalOutput.innerHTML = `

<pre class="terminal-banner">

Healthcare IoT Defense Honeypot Network

SOC Terminal Cleared

Type HELP

</pre>

`;

}

/* ==========================================
   LIVE EVENT FEED
========================================== */

function initializeLiveEvents() {

    const container =
        document.getElementById(
            "liveEvents"
        );

    if (!container)
        return;

    const events = [

        "[INFO] Honeypot Online",

        "[INFO] Device Registered",

        "[INFO] IOC Updated",

        "[WARNING] SSH Login Attempt",

        "[WARNING] Telnet Scan Detected",

        "[CRITICAL] Modbus Exploit Attempt",

        "[INFO] Threat Feed Updated",

        "[INFO] Analyst Login",

        "[INFO] Monitoring Active"

    ];

    setInterval(
        () => {

            const item =
                document.createElement(
                    "div"
                );

            item.textContent =
                events[
                    Math.floor(
                        Math.random() *
                        events.length
                    )
                ];

            container.prepend(
                item
            );

            while (
                container.children.length > 8
            ) {

                container.removeChild(
                    container.lastChild
                );

            }

        },
        5000
    );

}

/* ==========================================
   COMMAND SHORTCUTS
========================================== */

document.addEventListener(
    "keydown",
    function(e) {

        if (
            e.ctrlKey &&
            e.key === "l"
        ) {

            e.preventDefault();

            clearTerminal();

        }

    }
);

/* ==========================================
   AUTO FOCUS
========================================== */

document.addEventListener(
    "click",
    () => {

        if (
            terminalInput
        ) {

            terminalInput.focus();

        }

    }
);

/* ==========================================
   STARTUP MESSAGE
========================================== */

setTimeout(
    () => {

        appendLine(
            "[SYSTEM] Flask Backend Connected",
            "command-success"
        );

    },
    1000
);

setTimeout(
    () => {

        appendLine(
            "[SYSTEM] Command Engine Ready",
            "command-success"
        );

    },
    1500
);

setTimeout(
    () => {

        appendLine(
            "Type HELP for available commands",
            "command-info"
        );

    },
    2000
);