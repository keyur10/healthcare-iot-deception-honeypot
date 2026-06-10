document.addEventListener(
    "DOMContentLoaded",
    () => {

        const searchInput =
            document.getElementById(
                "searchInput"
            );

        if (!searchInput) return;

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
);