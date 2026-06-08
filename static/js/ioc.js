const searchInput =
    document.getElementById(
        "iocSearch"
    );

const rows =
    document.querySelectorAll(
        "#iocTable tr"
    );

searchInput.addEventListener(
    "keyup",
    () => {

        const value =
            searchInput.value
            .toLowerCase();

        rows.forEach(
            row => {

                row.style.display =
                    row.innerText
                    .toLowerCase()
                    .includes(value)
                    ? ""
                    : "none";

            }
        );

    }
);