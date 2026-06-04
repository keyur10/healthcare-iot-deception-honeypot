document.addEventListener(
    "DOMContentLoaded",
    () => {

        initializeTheme();

    }
);

/* ==================================================
   THEME
================================================== */

function initializeTheme() {

    const savedTheme =
        localStorage.getItem(
            "soc-theme"
        );

    if (savedTheme) {

        document.body.setAttribute(
            "data-theme",
            savedTheme
        );

    }

}

function toggleTheme() {

    const currentTheme =
        document.body.getAttribute(
            "data-theme"
        );

    const newTheme =
        currentTheme === "light"
            ? "dark"
            : "light";

    document.body.setAttribute(
        "data-theme",
        newTheme
    );

    localStorage.setItem(
        "soc-theme",
        newTheme
    );

    showThemeNotification(
        `Theme changed to ${newTheme.toUpperCase()}`
    );

}

function showThemeNotification(
    message
) {

    if (
        typeof showNotification ===
        "function"
    ) {

        showNotification(
            message,
            "info"
        );

    }

}