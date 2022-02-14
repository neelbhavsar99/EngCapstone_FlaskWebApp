document.getElementById('buttonboxbackleft').addEventListener("click", function leftButton() {
    fetch("", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            direction: "Left"
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
            direction: "Right"
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
            direction: "Stop"
        })
    })
});
