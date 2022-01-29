window.onblur = function () {
    pause();
}
window.onfocus = function () {
    play();
}
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

window.onload = function () {
    createProgressbar("{{ duration }}", function () {
        alert('{{ duration }}s progressbar is finished!');
    });
};

function pause() {
    progressbar.querySelector('.inner').style.animationPlayState = 'paused';
}

function play() {
    progressbar.querySelector('.inner').style.animationPlayState = 'running';
}