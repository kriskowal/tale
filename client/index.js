
include('browser.js');
observe(
    document.getElementById('playButton'),
    'click',
    function () {
        this.stop();
        alert('here');
    }
);

