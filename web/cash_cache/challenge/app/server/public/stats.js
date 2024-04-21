window.onload = async () => {
    let resp = await fetch("/");
    console.log("response.headers =", resp.headers);
    const STATS_ELEMS = {
        'x-cachedroutes': 'You visited _ routes!',
        'x-cashspent': 'You spent _ dollars!'
    };
    stats.innerHTML = '<h2>Cash Stats!</h2><br>'
    resp.headers.forEach((val, key) => {
        console.log(key)
        if (key in STATS_ELEMS) {
            const ELEM = document.createElement('p')
            ELEM.innerText = STATS_ELEMS[key].replace('_', val)
            stats.appendChild(ELEM)
        }
    })
    stats.appendChild(document.createElement('br'))
}