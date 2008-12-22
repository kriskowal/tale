
//include('debug.js');
include('base.js');
include('select.js');
include('browser.js');
include('widget/console.js');
var json = require("json.js");
var http = require('http.js');

var quantum = 1000;
var timeout = 10000;

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
var request;

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
    if (!response.isOk()) {
        throw new Error("receive should only get ok responses");
    }
    response = response.getText();
    response = json.decode(response);
    if (!connected)
        note(connectedNotes.next());
    connected = true;
    forEach(response.messages, function (message) {
        if (message.html)
            note(message.html);
        if (message.sound)
            sound(message.sound).play();
    });
    tick();
};

var receiveError = function (response) {
    if (connected)
        note(disconnectedNotes.next() + ' ' + response.getStatus());
    connected = false;
    tick();
};

var commandError = function (response) {
    note('Tale did not accept your command.');
    tick();
};

var tick = function () {
    setTimeout(function () {
        if (request) request.abort();
        request = http.request({
            'url': '/session/push.json',
            'content': json.encode(n),
            'ok': receive,
            'error': receiveError,
            'asynchronous': true
        });
    }, quantum);
};

tick();

console.observe('command', function (command) {
    if (!connected) {
        note(
            "Sorry, the command, " + enquote(command) +
            ", may not have been received because Tale " +
            "does not appear to be listening."
        );
    }
    if (request) request.abort();
    request = http.request({
        'url': '/session/command.json',
        'method': 'POST',
        'content': json.encode({
            'n': n,
            'command': command
        }),
        'ok': receive,
        'error': commandError,
        'asynchronous': true
    });
});

commandLine.focus();

