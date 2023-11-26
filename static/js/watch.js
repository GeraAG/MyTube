var intToString = num => {
    num = num.toString().replace(/[^0-9.]/g, '');
    if (num < 1000) {
        return num;
    }
    let si = [
      {v: 1E3, s: "K"},
      {v: 1E6, s: "M"},
      {v: 1E9, s: "B"}
      ];
    let index;
    for (index = si.length - 1; index > 0; index--) {
        if (num >= si[index].v) {
            break;
        }
    }
    return (num / si[index].v).toFixed(2).replace(/\.0+$|(\.[0-9]*[1-9])0+$/, "$1") + si[index].s;
};

function likeView() {
    const elem = document.getElementById("likes");
    console.log(elem);
    elem.innerHTML = intToString(Number(elem.innerHTML));
}

function videoView() {
    const elem = document.getElementById("views-digits");
    console.log(elem)
    elem.innerHTML = intToString(Number(elem.innerHTML));
}

window.onload = function() {
    likeView();
    videoView();
};
