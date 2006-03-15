
var mage = (function () {

    var urlBase = '';
    var session = '';
    var pollingInterval = 1000;
    var connectStatus = 0;
    var initialConnectStatus = 0;

    var enqueueMessage = function (message) {
        messageBuffer.enqueueMessage(message);
    }
    var enqueueException = function (x) {
        messageBuffer.enqueueException(x);
    }

    try {

        var poll = function (command) {
            var request = new XMLHttpRequest();
            var url = urlBase + '/state?session=' + escape(session);
            if (arguments.length && command) {
                url += '&command=' + escape(command);
            }
            request.onreadystatechange = function () {
                try {
                    if (request.readyState == 4) {
                        if (request.status == 200) {

                            // maintain connection status
                            if (connectStatus == 0 && initialConnectStatus == 1) {
                                enqueueMessage('Your connection to the <b>server</b> has been <b>restored</b>.')
                            }
                            connectStatus = 1;
                            initialConnectStatus = 1;

                            var response = request.responseXML;
                            session = response.getElementsByTagName('session')[0].firstChild.data;
                            var messages = response.getElementsByTagName('messages')[0];
                            window.title = response.getElementsByTagName('title')[0].firstChild.data;
                            var message = messages.firstChild;
                            while (message) {
                                enqueueMessage(message.firstChild.data);
                                message = message.nextSibling;
                            }
                        } else {
                            enqueueException('Server request status was ' + request.status + ' for ' + url)
                        }
                    }
                } catch (x) {
                    if (connectStatus == 1) {
                        enqueueMessage('You have been <b>disconnected</b> from the <b>server</b>.');
                    }
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



}());

