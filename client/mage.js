window.mage = (function () {

var urlBase = '';
var session = '';
var pollingInterval = 1000;
var connectStatus = 0;
var initialConnectStatus = 0;
var request = 0;
var trials = 0;
var trialMax = 20;
var silent = 'no';

var enqueueMessage = window.messageBuffer.enqueueMessage;
var enqueueException = window.messageBuffer.enqueueException;

var commandBox = document.getElementById('command');
var promptBox = document.getElementById('prompt');

try {

    var poll = function (command) {

        // assure that only one xmlhttprequest is pending at any time
        if (request !== 0) {
            trials++;
            if (trials > trialMax) {
                trials = 0;
                request.abort()
                if (request.command) {
                    enqueueException(
                        'Failed to send the <b>command</b>, <tt>' +
                        request.command + 
                        '</tt> to the <b>server</b>.'
                    );
                }
            } else {
                if (arguments.length && command) {
                    // if this supposed to send a command, send the
                    // request despite the pending message.
                } else {
                    return;
                }
            }
        }

        request = new XMLHttpRequest();
        var url = urlBase + '/session?session=' + escape(session);
        if (arguments.length && command) {
            url += '&command=' + escape(command);
            request.command = command;
        }
        request.onreadystatechange = function () {
            try {
                if (request !== 0 && request.readyState == 4) {
                    if (request.status == 200) {

                        // maintain connection status
                        if (connectStatus == 0 && initialConnectStatus == 1) {
                            enqueueMessage(
                                'Your connection to the <b>server</b> ' +
                                'has been <b>restored</b>.'
                            )
                        }
                        connectStatus = 1;
                        initialConnectStatus = 1;

                        var response = request.responseXML;
                        session = response.getElementsByTagName('session')[0].firstChild.data;
                        var prompt = response.getElementsByTagName('prompt')[0].firstChild.data;
                        var silent = response.getElementsByTagName('silent')[0].firstChild.data;
                        var title = response.getElementsByTagName('title')[0].firstChild.data;
                        var messages = response.getElementsByTagName('messages')[0];
                        var overlays = response.getElementsByTagName('overlays')[0];

                        promptBox.innerHTML = prompt;

                        messageBuffer.setSilent(silent == 'yes')

                        messageBuffer.setTitle(title);

                        var message = messages.firstChild;
                        while (message) {
                            enqueueMessage(message.firstChild.data);
                            message = message.nextSibling;
                        }

                        var overlay = overlays.firstChild;
                        while (overlay) {
                            window.overlays.update(overlay.firstChild);
                            overlay = overlay.nextSibling;
                        }

                        // set the request object to zero so that
                        //  we dont abort it next time through the polling
                        //  loop.
                        request = 0;

                    } else {
                        enqueueException(
                            'The <b>server</b> unexpectedly responded ' +
                            'with an HTTP errors status, ' +
                            '<tt>' + request.status + '</tt>, ' + 
                            'for <tt>' + url + '</tt>.'
                        )
                    }
                }

            } catch (x) {
                if (request != 0 && connectStatus == 1) {
                    enqueueMessage(
                        'You have been <b>disconnected</b> ' + 
                        'from the <b>server</b> ' +
                        'or are experiencing <b>lag</b>.'
                    );
                }
                throw(x);
                connectStatus = 0;
            }

        }
        request.open("GET", url, true);
        request.send('');

    }

    messageBuffer.handleCommand = poll;
    setInterval(function () {poll()}, pollingInterval);
    poll();

} catch (x) {
    enqueueException(x);
}

return this;
}());
