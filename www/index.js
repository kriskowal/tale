
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
var playing;
var musicWidget = document.getElementById('music')
observe(musicWidget, 'click', function () {
    if (!clicked) {
        sound = require('sound.js');
        sound.ready.observe(function () {
            sound.play('music/6-1-euia-adventure.mp3');
            insertClass(musicWidget, 'play');
        });
        clicked = true;
        playing = true;
    } else {
        sound.ready.observe(function () {
            sound.toggle();
            if (playing) {
                removeClass(musicWidget, 'play');
            } else {
                insertClass(musicWidget, 'play');
            }
            playing = !playing;
        });
    }
});
insertClass(musicWidget, 'ready');

// prefetch
new Image().src = "/art/pause.png";

if (isSafari || isFirefox) {

    var start = new Date().getTime();

    var quantum = isSafari ? 200 : 1000;
    var rate = Math.PI * 2 / 1000 / 4;

    var animate = function (rate, functor) {
        var tick = function () {
            try {
                var position = (new Date().getTime() - start) * rate / quantum;
                functor(position);
            } finally {
                setTimeout(tick, quantum);
            }
        };
        tick();
    };

    var dyo = new Image();
    var dya = new Image();
    dyo.src = "/art/dyo.png";
    dya.src = "/art/dya.png";
    dya.onload = function () {dya.ready = true; ready()};
    dyo.onload = function () {dyo.ready = true; ready()};
    var ready = function () {
        if (!dya.ready || !dyo.ready)
            return;

        var canvas = document.createElement('canvas');
        canvas.width = 360;
        canvas.height = 360;

        // legerdemain
        var parentNode = img.parentNode;
        parentNode.removeChild(img);
        parentNode.appendChild(canvas);

        var context = canvas.getContext('2d');
        context.translate(180, 180);
        context.drawImage(img, -180, -180, 360, 360);

        animate(rate, function (delta) {
            context.save();
            context.clearRect(-180, -180, 360, 360);
            context.drawImage(dyo, -180, -180, 360, 360);
            context.rotate(delta);
            context.drawImage(dya, -180, -180, 360, 360);
            context.restore();
        });

    };

}

