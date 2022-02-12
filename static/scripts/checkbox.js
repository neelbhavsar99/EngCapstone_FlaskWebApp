var localIp = "http://192.168.2.61:5000/";
document
    .querySelector("input")
    .addEventListener("click", e => {
        fetch(localIp, {
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                mode: Number(e.target.checked)
            })
        })/*
            .then(res => {
                if (!res.ok) {
                    throw Error(res.status);
                }
                console.log(res);
                return res.json();
            })
            .then(({ data: { val } }) => {
                //console.log(val);
                //const res = document.querySelector(".result");
                //res.innerText = `client got: ${val}`;
            })
            .catch(err => console.error(err))*/
            ;
    });