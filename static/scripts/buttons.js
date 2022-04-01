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

document.getElementById('buttonboxbackstop').addEventListener("click", function stopButton() {
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

document.getElementById('startRecording').addEventListener("click", function startRecordingButton() {
    fetch("", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            startRecording: true
        })
    })
    $('#recButton').removeClass("notRec");
    $('#recButton').addClass("Rec");
});

document.getElementById('stopRecording').addEventListener("click", function stopRecordingButton() {
    fetch("", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            saveRecording: true
        })
    })
    $('#recButton').removeClass("Rec");
    $('#recButton').addClass("notRec");
});


$('#recButton').addClass("notRec");

// $('#recButton').click(function () {
//     if ($('#recButton').hasClass('notRec')) {
//         $('#recButton').removeClass("notRec");
//         $('#recButton').addClass("Rec");
//     }
//     else {
//         $('#recButton').removeClass("Rec");
//         $('#recButton').addClass("notRec");
//     }
// });	