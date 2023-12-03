function showHide() {
    var e = document.getElementsByClassName('playlist-description')[0];
    e.classList.toggle("visible");
    var bt = document.getElementById("showhideButton")
    if (e.classList.contains("visible")) {
        bt.innerHTML = "Show Less";
    } else {
        bt.innerHTML = "...more";
    };
};

function isOverflown(element){
    return element.scrollHeight > element.clientHeight || element.scrollWidth > element.clientWidth;
};

function hideButton() {
    var e = document.getElementsByClassName('playlist-description')[0];
    if (isOverflown(e)) {
        document.getElementById("showhideButton").classList.toggle("hidden");
    };
};

window.onload = function() {
    hideButton();
};
