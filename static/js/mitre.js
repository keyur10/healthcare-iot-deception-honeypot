document.addEventListener(
    "DOMContentLoaded",
    () => {

        startMitreRefresh();

    }
);

let mitreRefresh = null;

function startMitreRefresh() {

    updateMitreData();

    mitreRefresh = setInterval(

        updateMitreData,

        10000

    );

}

async function updateMitreData() {

    try {

        const response =
            await fetch(
                "/api/mitre"
            );

        const data =
            await response.json();

        updateEventFeed(
            data.events
        );

    }

    catch(error) {

        console.error(
            "MITRE Update Failed",
            error
        );

    }

}

function updateEventFeed(
    events
) {

    const feed =
        document.querySelector(
            ".event-feed"
        );

    if (
        !feed ||
        !events
    ) {

        return;

    }

    feed.innerHTML = "";

    events.reverse().forEach(
        event => {

            const div =
                document.createElement(
                    "div"
                );

            div.className =
                "event-item";

            div.innerHTML = `

                <div class="event-technique">

                    ${event.attack_type}

                </div>

                <div class="event-ip">

                    ${event.source_ip}

                </div>

                <div class="event-risk">

                    ${event.risk}

                </div>

            `;

            feed.appendChild(
                div
            );

        }
    );

}

/* Auto Refresh When Tab Returns */

document.addEventListener(
    "visibilitychange",
    () => {

        if (
            !document.hidden
        ) {

            updateMitreData();

        }

    }
);