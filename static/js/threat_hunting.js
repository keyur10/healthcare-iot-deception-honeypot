function huntIOC(){

    const query =
        document.getElementById(
            "huntQuery"
        ).value;

    if(!query){

        alert(
            "Enter IP, Domain or Hash"
        );

        return;
    }

    fetch(
        "/api/threat-hunt?q=" +
        encodeURIComponent(query)
    )
    .then(response => response.json())
    .then(data => {

        const table =
            document.getElementById(
                "huntResults"
            );

        table.innerHTML = "";

        data.forEach(item => {

            table.innerHTML += `
                <tr>
                    <td>${item.indicator}</td>
                    <td>${item.type}</td>
                    <td>${item.source}</td>
                    <td>${item.severity}</td>
                </tr>
            `;

        });

    });

}