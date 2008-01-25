/*preamble

    Copyright (c) 2002-2007 Kris Kowal <http://cixar.com/~kris.kowal>
    MIT License
    
    The license terms are stated in full in <license.txt> and at the end
    of all source files.

*/

include('boost.js');
include('browser.js');
include('widget.js');
include('color.js');
include(names);

var head; 
var style;
var setColorScheme = function (fore, back) {
    if (no(head)) head = document.getElementsByTagName('head')[0];
    if (style) head.removeChild(style);
    style = document.createElement('style');
    var text = document.createTextNode(
        'body { ' +
            'color: ' + fore + '; ' +
            'background-color: ' + back +
        '}'
    );
    style.appendChild(text);
    head.appendChild(style);
};

var f = Color('#46b3d3');
var b = Color();
b.setHue((f.getHue(1) + .666) % 1, 1);
b.setSaturation(f.getSaturation(1), 1);
setInterval(function () {
    var t = (Math.sin(new Date().getTime() / 1000 / 15 * 2 * Math.PI) + 1) / 2;
    f.setSaturation(1 - t, 1);
    f.setLightness(.5 + t / 2, 1);
    b.setLightness(.5 + -t / 2, 1);
    setColorScheme(b.string(), f.string());
}, 100);

/*
this.Console = type([Widget], function () {
    this.init = function (element) {
        this.getSuper(Console).init(element);
        element.innerHTML = 'Here';
        log('here');
    };
});
*/

/*license

    Credits
    =======
    
    See <credit.txt> for a complete list of
    contributions and their licenses.  All contributions are provided
    under permissive licenses including MIT, BSD, Creative Commons
    Attribution 2.5, Public Domain, or Unrestricted.
    
    
    License
    =======
    
    Copyright (c) 2002-2007 Kris Kowal <http://cixar.com/~kris.kowal>
    MIT License
    
    
    MIT License
    -----------
    
    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation
    files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use,
    copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following
    conditions:
    
    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.

*/

