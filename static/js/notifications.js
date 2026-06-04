document.addEventListener(
    "DOMContentLoaded",
    () => {

        initializeNotifications();

    }
);

/* ==================================================
   NOTIFICATIONS
================================================== */

function initializeNotifications() {

    if (
        !document.getElementById(
            "notification-container"
        )
    ) {

        const container =
            document.createElement(
                "div"
            );

        container.id =
            "notification-container";

        container.style.position =
            "fixed";

        container.style.top =
            "20px";

        container.style.right =
            "20px";

        container.style.zIndex =
            "9999";

        container.style.width =
            "350px";

        document.body.appendChild(
            container
        );

    }

}

/* ==================================================
   SHOW
================================================== */

function showNotification(
    message,
    type = "info"
) {

    const container =
        document.getElementById(
            "notification-container"
        );

    if (!container) {
        return;
    }

    const notification =
        document.createElement(
            "div"
        );

    const classes = {

        success:
            "alert-success",

        danger:
            "alert-danger",

        warning:
            "alert-warning",

        info:
            "alert-info"

    };

    notification.className =
        `alert ${
            classes[type] ||
            classes.info
        } shadow-lg mb-2`;

    notification.innerHTML = `

        <div class="d-flex justify-content-between align-items-center">

            <span>

                ${message}

            </span>

            <button
                class="btn-close">
            </button>

        </div>

    `;

    container.prepend(
        notification
    );

    notification
        .querySelector(
            ".btn-close"
        )
        .addEventListener(
            "click",
            () => {

                notification.remove();

            }
        );

    setTimeout(
        () => {

            notification.remove();

        },
        5000
    );

}

/* ==================================================
   HELPERS
================================================== */

function notifySuccess(
    message
) {

    showNotification(
        message,
        "success"
    );

}

function notifyError(
    message
) {

    showNotification(
        message,
        "danger"
    );

}

function notifyWarning(
    message
) {

    showNotification(
        message,
        "warning"
    );

}

function notifyInfo(
    message
) {

    showNotification(
        message,
        "info"
    );

}
document.addEventListener(
    "DOMContentLoaded",
    () => {

        setTimeout(() => {

            document
                .querySelectorAll(
                    ".auto-dismiss-alert"
                )
                .forEach(alert => {

                    const bsAlert =
                        bootstrap.Alert.getOrCreateInstance(
                            alert
                        );

                    bsAlert.close();

                });

        }, 2000);

    }
);