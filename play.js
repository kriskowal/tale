with (require('base.js')) {
with (require('browserBase.js')) {
with (require('animate.js')) {
with (require('transitions.js')) {
with (require('color.js')) {
(function () { /* closure */

this.Play = type(function () {
    this.init = function (element) {
        log('here');
    };
});

var getBackgroundColor = function () {
    return getStyle(document.body, 'backgroundColor');
};

var setBackgroundColor = function () {
    var backgroundColor = Color(getBackgroundColor());
    var newColor = Color(backgroundColor);
    newColor.setHue(Math.random(), 1, ordinal);
    animate(
        10000,
        compose(transition(backgroundColor, newColor), reversed(cubic)), 
        function (color) {
            document.body.style.backgroundColor = color.string();
        }
    );
};

var chironscript = require('chironscript.js');
setBackgroundColor();
setInterval(setBackgroundColor, 10000);

}).call(this);
}}}}} /* with */
