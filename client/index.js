
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
    handle = setInterval(function () {
        try {
            context.clearRect(-180, -180, 360, 360);
            context.rotate(Math.PI * 2 / 1000 / 5);
            context.drawImage(img, -123, -180, 261, 300);
        } catch (x) {
            error(x.message);
            clearInterval(handle);
        }
    }, 250);
}

