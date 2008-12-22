
include('environment.js');
include('browser.js');

var img = document.getElementById('tale');
var handle;

observe(
    document.getElementById('playButton'),
    'click',
    function () {
        this.stop();
        if (handle !== undefined)
            clearInterval(handle);
        require('./play.js');
    }
);

var clicked;
var sound;
observe(img.parentNode, 'click', function () {
    if (!clicked) {
        sound = require('sound.js');
        sound.ready.observe(function () {
            sound.play('music/6-1-euia-adventure.mp3');
        });
        clicked = true;
    } else {
        sound.ready.observe(function () {
            sound.toggle();
        });
    }
});

img.parentNode.style.cursor = 'pointer';

if (isSafari || isFirefox) {

    var quantum = isSafari ? 100 : 1000;
    var animate = function (rate, functor) {
        var lastPosition = new Date().getTime();
        var tick = function () {
            try {
                var position = new Date().getTime() * rate / quantum;
                functor(position - lastPosition);
                lastPosition = position;
            } finally {
                setTimeout(tick, quantum);
            }
        };
        tick();
    };

    var canvas = document.createElement('canvas');
    canvas.width = 360;
    canvas.height = 360;

    // legerdemain
    var parentNode = img.parentNode;
    parentNode.removeChild(img);
    parentNode.appendChild(canvas);

    var context = canvas.getContext('2d');
    context.translate(180, 180);
    context.rotate(Math.PI * 2 / 1000 / 5);

    var lastPosition;
    animate(Math.PI * 2 / 1000 / 5, function (delta) {
        context.clearRect(-180, -180, 360, 360);
        context.rotate(delta);
        context.drawImage(img, -123, -180, 261, 300);
    });

}

