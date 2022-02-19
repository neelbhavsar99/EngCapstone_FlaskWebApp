document.getElementById('buttonboxbackleft').addEventListener("click", function leftButton() {
    fetch("", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            direction: "left"
        })
    })
});

document.getElementById('buttonboxbackright').addEventListener("click", function rightButton() {
    fetch("", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            direction: "right"
        })
    })
});

document.getElementById('buttonboxbackstop').addEventListener("click", function leftButton() {
    fetch("", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            direction: "stop"
        })
    })
});
