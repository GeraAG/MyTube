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
    elem.innerHTML = intToString(Number(elem.innerHTML));
};

function videoView() {
    const elem = document.getElementById("views-digits");
    elem.innerHTML = intToString(Number(elem.innerHTML));
};

function commentLikeView() {
    document.querySelectorAll('.comment-like').forEach(function(text) {
        text.innerHTML = intToString(Number(text.innerHTML));
    });
};

function showHide() {
    var e = document.getElementsByClassName('description-text')[0];
    e.classList.toggle("visible");
    var bt = document.getElementById("showhideButton")
    if (e.classList.contains("visible")) {
        bt.innerHTML = "Show Less";
    } else {
        bt.innerHTML = "...more";
    }
}

function isOverflown(element){
    return element.scrollHeight > element.clientHeight || element.scrollWidth > element.clientWidth;
}

function showComment() {
    document.querySelectorAll('.content-container').forEach(function(comment) {
        if (isOverflown(comment.querySelectorAll("div")[0])) {
            comment.querySelectorAll("div")[1].classList.toggle("hidden");

            comment.querySelectorAll("div")[1].addEventListener("click", (e) => {
                if (e.currentTarget.parentNode.querySelectorAll("div")[0].classList.toggle("visible")) {
                    e.currentTarget.innerHTML = "Show Less";
                } else {
                    e.currentTarget.innerHTML = "...Read More";
                }
            });
        }

    });
};

window.onload = function() {
    likeView();
    videoView();
    commentLikeView();
    showComment();

};
