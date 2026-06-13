document.addEventListener(
    "DOMContentLoaded",
    () => {

        startAlertRefresh();

    }
);

function startAlertRefresh(){

    setInterval(

        loadAlerts,

        5000

    );

}
async function responseAction(
    action,
    target
){

    try{

        const response =
            await fetch(
                "/api/alert-action",
                {
                    method:"POST",

                    headers:{
                        "Content-Type":
                        "application/json"
                    },

                    body:JSON.stringify({

                        action:action,

                        target:target

                    })

                }
            );

        const data =
            await response.json();

        alert(
            data.message
        );

    }

    catch(error){

        console.error(
            error
        );

        alert(
            "Action Failed"
        );

    }

}

async function loadAlerts(){

    try{

        const response =
            await fetch(
                "/api/alerts"
            );

        const data =
            await response.json();

        console.log(
            data
        );

    }

    catch(error){

        console.error(
            error
        );

    }

}

async function responseAction(
    action,
    target
){

    try{

        const response =
            await fetch(
                "/api/alert-action",
                {
                    method:"POST",

                    headers:{
                        "Content-Type":
                        "application/json"
                    },

                    body:
                    JSON.stringify({

                        action:
                            action,

                        target:
                            target

                    })
                }
            );

        const data =
            await response.json();

        alert(
            data.message
        );

    }

    catch(error){

        alert(
            "Action Failed"
        );

    }

}