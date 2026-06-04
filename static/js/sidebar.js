document.addEventListener(
    "DOMContentLoaded",
    () => {

        initializeSidebar();

    }
);

/* ==================================================
   SIDEBAR
================================================== */

function initializeSidebar() {

    highlightActiveLink();

    initializeSidebarToggle();

}

/* ==================================================
   ACTIVE MENU
================================================== */

function highlightActiveLink() {

    const currentPath =
        window.location.pathname;

    document
        .querySelectorAll(
            ".sidebar-menu a"
        )
        .forEach(link => {

            const href =
                link.getAttribute(
                    "href"
                );

            if (
                href === currentPath
            ) {

                link.classList.add(
                    "active"
                );

            }

        });

}

/* ==================================================
   MOBILE TOGGLE
================================================== */

function initializeSidebarToggle() {

    const toggle =
        document.getElementById(
            "sidebar-toggle"
        );

    const sidebar =
        document.querySelector(
            ".sidebar"
        );

    if (
        !toggle ||
        !sidebar
    ) {

        return;

    }

    toggle.addEventListener(
        "click",
        () => {

            sidebar.classList.toggle(
                "active"
            );

        }
    );

    document.addEventListener(
        "click",
        event => {

            if (
                window.innerWidth > 992
            ) {

                return;

            }

            if (
                !sidebar.contains(
                    event.target
                ) &&
                !toggle.contains(
                    event.target
                )
            ) {

                sidebar.classList.remove(
                    "active"
                );

            }

        }
    );

}