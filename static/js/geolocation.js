const map = L.map(
    "attackMap"
).setView(
    [20, 78],
    3
);

L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        attribution:
        "&copy; OpenStreetMap"
    }
).addTo(map);

document
.querySelector(".lookup-form button")
.addEventListener(
    "click",
    lookupIP
);

async function lookupIP() {

    const ip =
        document
        .getElementById("ipLookup")
        .value
        .trim();

    if (!ip) {

        alert(
            "Enter IP Address"
        );

        return;

    }

    const response =
        await fetch(
            `/api/geolocate/${ip}`
        );

    const data =
        await response.json();

    if (
        data.status !== "success"
    ) {

        return;

    }

    document.querySelector(
        ".lookup-result"
    ).innerHTML = `

        <strong>IP:</strong> ${data.ip}<br>
        <strong>Country:</strong> ${data.country}<br>
        <strong>City:</strong> ${data.city}<br>
        <strong>ISP:</strong> ${data.isp}

    `;

    L.marker([
        data.lat,
        data.lon
    ])
    .addTo(map)
    .bindPopup(
        `${data.ip}<br>${data.country}`
    )
    .openPopup();

    map.setView(
        [data.lat, data.lon],
        6
    );

}