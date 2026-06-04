/* ==================================================
   SESSION TIMEOUT
================================================== */

const WARNING_TIME =
    4 * 60 * 1000;

const LOGOUT_TIME =
    5 * 60 * 1000;

let warningTimer;
let logoutTimer;

/* ==================================================
   RESET
================================================== */

function resetSessionTimers() {

    clearTimeout(
        warningTimer
    );

    clearTimeout(
        logoutTimer
    );

    warningTimer =
        setTimeout(
            showWarning,
            WARNING_TIME
        );

    logoutTimer =
        setTimeout(
            logoutUser,
            LOGOUT_TIME
        );

}

/* ==================================================
   WARNING
================================================== */

function showWarning() {

    const existing =
        document.getElementById(
            "session-warning"
        );

    if (existing) {
        return;
    }

    const modal =
        document.createElement(
            "div"
        );

    modal.id =
        "session-warning";

    modal.innerHTML = `

        <div
            style="
                position:fixed;
                inset:0;
                background:rgba(0,0,0,.75);
                z-index:99999;
                display:flex;
                justify-content:center;
                align-items:center;
            ">

            <div
                style="
                    background:#111827;
                    color:white;
                    padding:30px;
                    border-radius:15px;
                    text-align:center;
                    width:400px;
                ">

                <h4>

                    Session Expiring

                </h4>

                <p>

                    You will be logged out in
                    1 minute.

                </p>

                <button
                    id="stay-logged-in"
                    class="btn btn-info">

                    Stay Logged In

                </button>

            </div>

        </div>

    `;

    document.body.appendChild(
        modal
    );

    document
        .getElementById(
            "stay-logged-in"
        )
        .addEventListener(
            "click",
            () => {

                modal.remove();

                resetSessionTimers();

            }
        );

}

/* ==================================================
   LOGOUT
================================================== */

function logoutUser() {

    window.location.href =
        "/logout";

}

/* ==================================================
   USER ACTIVITY
================================================== */

[
    "mousemove",
    "mousedown",
    "keypress",
    "scroll",
    "click",
    "touchstart"
].forEach(event => {

    document.addEventListener(
        event,
        resetSessionTimers,
        true
    );

});

/* ==================================================
   INIT
================================================== */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        resetSessionTimers();

    }
);