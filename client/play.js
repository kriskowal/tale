
//include('debug.js');
include('minidebug.js');
include('base.js');
include('select.js');
include('browser.js');
include('widget/console.js');
var json = require("json.js");
var http = require('http.js');

var sound = require('sound.js');
sound.ready.observe(function () {
});

var buffer = document.getElementById('buffer');
var viewport = document.body;
var prompt = tag('nobr', {'id': 'prompt'});
var commandLine = tag('input', {'type': 'textbox'});
var commandBar = tag(
    'table',
    {
        'id': 'commandBar',
        'classes': ['bottom', 'message', 'command']
    },
    [
        tag('tr', {}, [
            tag('td', {'class': 'A'}, [prompt]),
            tag('td', {'class': 'B'}, [commandLine])
        ])
    ]
);
var viewport = document.body;
buffer.parentNode.insertBefore(commandBar, buffer.nextSibling);
var console = Console(buffer, prompt, commandLine, viewport);

var menuBar = select('.menuBar').forEach(function (menuBar) {
    menuBar.parentNode.removeChild(menuBar);
});

var n = 0;

var note = function (html) {
    var p = document.createElement('p');
    p.innerHTML = html;
    console.output(p);
};

var connected = true;

var connectedNotes = add(iter([
    "Oh, Tale is listening now."
]), cycle([
    "Tale is listening again.",
    "Tale is back up.",
    "Tale is up."
]));

var disconnectedNotes = cycle([
    "The narrator does not appear to be listening.  " +
    "Don't feel unloved; it promises to return.",
    "Tale's not listening again.",
    "This is probably getting old, but Tale is down again.",
    "Sorry, Tale's down now."
])

var receive = function (response) {
    if (!connected)
        note(connectedNotes.next());
    connected = true;
    forEach(response.messages, function (message) {
        if (Number(message.n) >= n) {
            if (!no(message.html))
                note(message.html);
            if (!no(message.sound))
                sound(message.sound).play();
            n = Number(message.n) + 1;
        }
    });
};

var receiveError = function (response) {
    error('error ' + response.getStatus());
    if (connected)
        note(disconnectedNotes.next() + ' ' + response.getStatus());
    connected = false;
};

setInterval(function () {
    json.request({
        'url': '/session/',
        'method': 'POST',
        'content': json.format(n),
        'error': receiveError
    }, receive);
}, 1000);

console.observe('command', function (command) {
    if (!connected) {
        note(
            "Sorry, the command, " + enquote(command) +
            ", was not sent because the Tale server " +
            "does not appear to be listening."
        );
    } else {
        json.request({
            'url': '/session/command/',
            'method': 'POST',
            'content': json.format({
                'n': n,
                'command': command
            }),
            'error': receiveError
        }, receive);
    }
});

commandLine.focus();

