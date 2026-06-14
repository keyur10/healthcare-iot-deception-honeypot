document.addEventListener(
    "DOMContentLoaded",
    () => {

        // Search

        const searchInput =
            document.getElementById(
                "searchInput"
            );

        if (searchInput) {

            searchInput.addEventListener(
                "keyup",
                function () {

                    const filter =
                        this.value.toLowerCase();

                    const rows =
                        document.querySelectorAll(
                            "#honeypotTable tr"
                        );

                    rows.forEach(
                        row => {

                            row.style.display =
                                row.innerText
                                    .toLowerCase()
                                    .includes(filter)
                                    ? ""
                                    : "none";

                        }
                    );

                }
            );

        }

        // Delete Confirmation

        document
            .querySelectorAll(
                ".delete-btn"
            )
            .forEach(
                button => {

                    button.addEventListener(
                        "click",
                        event => {

                            if (
                                !confirm(
                                    "Delete this honeypot?"
                                )
                            ) {

                                event.preventDefault();

                            }

                        }
                    );

                }
            );

        // Auto Close Flash Messages

        const flashMessages =
            document.querySelectorAll(
                ".flash-message"
            );

        flashMessages.forEach(
            message => {

                setTimeout(
                    () => {

                        message.classList.add(
                            "flash-hide"
                        );

                        setTimeout(
                            () => {

                                message.remove();

                            },
                            400
                        );

                    },
                    3000
                );

            }
        );

        // Auto Refresh Events

        setInterval(
            () => {

                const eventFeed =
                    document.querySelector(
                        ".event-feed"
                    );

                if (
                    eventFeed
                ) {

                    eventFeed.scrollTop =
                        eventFeed.scrollHeight;

                }

            },
            5000
        );

    }
);