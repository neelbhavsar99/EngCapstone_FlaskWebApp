/**
 * Get the user IP throught the webkitRTCPeerConnection
 * @param onNewIP {Function} listener function to expose the IP locally
 * @return undefined
 */
/*
 function getUserIP(onNewIP) { //  onNewIp - your listener function for new IPs
    //compatibility for firefox and chrome
    var myPeerConnection = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection;
    var pc = new myPeerConnection({
        iceServers: []
    }),
    noop = function() {},
    localIPs = {},
    ipRegex = /([0-9]{1,3}(\.[0-9]{1,3}){3}|[a-f0-9]{1,4}(:[a-f0-9]{1,4}){7})/g,
    key;

    function iterateIP(ip) {
        if (!localIPs[ip]) onNewIP(ip);
        localIPs[ip] = true;
    }

     //create a bogus data channel
    pc.createDataChannel("");

    // create offer and set local description
    pc.createOffer(function(sdp) {
        sdp.sdp.split('\n').forEach(function(line) {
            if (line.indexOf('candidate') < 0) return;
            line.match(ipRegex).forEach(iterateIP);
        });
        
        pc.setLocalDescription(sdp, noop, noop);
    }, noop); 

    //listen for candidate events
    pc.onicecandidate = function(ice) {
        if (!ice || !ice.candidate || !ice.candidate.candidate || !ice.candidate.candidate.match(ipRegex)) return;
        ice.candidate.candidate.match(ipRegex).forEach(iterateIP);
    };window.addEventListener('DOMContentLoaded', init);

    function init() {
        const form = document.querySelector('[data-calc-form]');
        const textInput = document.querySelector('[name=text]');
        const preview = document.querySelector('[data-preview]');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const text = textInput.value;
            const results = await fetchEstimations(text);
            preview.textContent = JSON.stringify(results, null, 4);
            console.log(results);
        });
    }

    async function fetchEstimations(text) {
        const payload = new FormData();
        payload.append('text', text);

        const res = await fetch('/calc', {
            method: 'post',
            body: payload
        });
        const estimation = await res.json();
        return estimation;
    }
}

// Usage

getUserIP(function(ip){
		document.getElementById("ip").innerHTML = 'Got your IP ! : '  + ip + " | verify in http://www.whatismypublicip.com/";
});
*/