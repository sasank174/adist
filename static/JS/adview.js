// window.onblur = function () {
//     pause();
// }
// window.onfocus = function () {
//     play();
// }


window.addEventListener("focus", function (event) {
    play();
}, false);
window.addEventListener("blur", function (event) {
    pause();
}, false);




var progressbar = document.querySelector('.progressbar');

function createProgressbar(duration, callback) {
    var progressbarinner = document.createElement('div');
    progressbarinner.className = 'inner';

    progressbarinner.style.animationDuration = duration + 's';
    if (typeof (callback) === 'function') {
        progressbarinner.addEventListener('animationend', callback);
    }

    progressbar.appendChild(progressbarinner);
    progressbarinner.style.animationPlayState = 'running';
}

var ids = []

window.onload = function () {
    var duration = document.querySelector('#duration').innerHTML;
    var iframes = document.getElementsByTagName('iframe');
    if (iframes.length <= 2) {
        alert("your browser is blocking ads. please disable adblocker and refresh the page or try another browser");
        window.location.href = '/';
    }
    createProgressbar(duration, function () {
        document.querySelector("#adpostform").style.display = "flex";
        // alert(duration + ' s progressbar is finished!');
    });

    document.querySelectorAll("li")
        .forEach(function (li) {
            ids.push(li.innerHTML);
        });

    const interval = setInterval(function () {
        clix();
    }, 3000);

    // clearInterval(interval);
};

function pause() {
    progressbar.querySelector('.inner').style.animationPlayState = 'paused';
}

function play() {
    progressbar.querySelector('.inner').style.animationPlayState = 'running';
}




function clix() {
    var frame1 = document.querySelectorAll("iframe")[0];
    var frame2 = document.querySelectorAll("iframe")[1];
    var frame3 = document.querySelectorAll("iframe")[2];
    var frame4 = document.querySelectorAll("iframe")[3];
    var frame5 = document.querySelectorAll("iframe")[4];
    var frame6 = document.querySelectorAll("iframe")[5];

    var random = Math.floor(Math.random() * ids.length);
    if (random == 5 || random == 6) {
        random = 1;
    } else if (random == 8) {
        document.querySelectorAll(".container-" + ids[random] + "__link")[0].click();
    } else {
        try {
            frame1.contentWindow.document.querySelector("#atLink-" + ids[random]).click();
        } catch (err) {}
        try {
            frame2.contentWindow.document.querySelector("#atLink-" + ids[random]).click();
        } catch (err) {}
        try {
            frame3.contentWindow.document.querySelector("#atLink-" + ids[random]).click();
        } catch (err) {}
        try {
            frame4.contentWindow.document.querySelector("#atLink-" + ids[random]).click();
        } catch (err) {}
        try {
            frame5.contentWindow.document.querySelector("#atLink-" + ids[random]).click();
        } catch (err) {}
        try {
            frame6.contentWindow.document.querySelector("#atLink-" + ids[random]).click();
        } catch (err) {}
    }

    // document.querySelectorAll(".container-1fe1cd691be6ddffcc749d27364ea449__link")[1].click()
    // document.querySelectorAll(".container-1fe1cd691be6ddffcc749d27364ea449__link")[2].click()
    // document.querySelectorAll(".container-1fe1cd691be6ddffcc749d27364ea449__link")[3].click()
}