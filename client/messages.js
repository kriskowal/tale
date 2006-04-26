window.messageBuffer = (function () {

// title
var titleBase = "Tale";
var hasFocus = 0;
var reviewingMessages = 0;
var titleSpinner = 0;
var titleTimeout = 1000;

// messages
var unviewedMessageCount = 0;
var messageCountMax = 64;
var pageYFudge = 10;
var lastPageYOffset = 0;

// commands
var silent = 0;
var commandsBefore = [];
var commandsAfter = [];

var commandBox = document.getElementById("command");
var titleBox = document.getElementsByTagName("title")[0];

// title

this.refreshTitle = function () {
    if ((!hasFocus || reviewingMessages) && unviewedMessageCount > 0) {
        if (titleSpinner) {
            document.title = "[" + unviewedMessageCount + "]  " + titleBase;
        } else {
            document.title = "[" + unviewedMessageCount + "] " + titleBase + " ";
        }
        titleSpinner = !titleSpinner;
        setTimeout(refreshTitle, titleTimeout);
    } else {
        document.title = titleBase;
        unviewedMessageCount = 0;
    }
};

this.setTitle = function(newTitle) {
    titleBase = newTitle;
    refreshTitle();
};

window.addEventListener(
    "focus",
    function () {
        hasFocus = 1;
        refreshTitle();
    },
    true
);

window.addEventListener(
    "blur",
    function () {
        hasFocus = 0;
        refreshTitle();
    },
    true
);

window.addEventListener(
    "load",
    function () {
        commandBox.focus();
    },
    true
);

window.addEventListener(
    "resize",
    function () {
        autoScroll();
        refreshTitle();
    },
    true
);


// messages 

this.enqueueNode = function(node) {
    var buffer = window.document.getElementById("buffer");
    var bufferEnd = window.document.getElementById("bufferEnd");
    buffer.insertBefore(node, bufferEnd);

    unviewedMessageCount++;

    reduceMessages();
    autoScroll();
    refreshTitle();
};

this.enqueueMessage = function(message) {
    if (message instanceof Image) {
        enqueueNode(message);
    } else {
        var node = window.document.createElement("p");
        node.innerHTML = message;
        enqueueNode(node);
    }
};

this.enqueueException = function(exception) {
    enqueueMessage('<b>Client Exception: </b>' + exception);
};

this.enqueuePage = function(message) {
	enqueueMessage(message);
};

this.enqueueUrl = function(url) {
	try {

		var req = new XMLHttpRequest();
		req.open('GET', url, false);
		req.send(null);
		
		if (req.status == 200) {
			var message = req.responseText;
			enqueueMessage(message);
		} else {
			enqueueException("Unable to load <tt>" + url + "</tt>");
		}
		
	} catch (x) {
		enqueueException(x + "<br/>Unable to load <tt>" + url + "</tt>");
        throw x;
	}
};

this.clearMessages = function() {
    var node = window.document.createElement("p");
    node.style.height = "100%";
    enqueueNode(node);
    reduceMessages();
    autoScroll();
};

this.reduceMessages = function() {
    var buffer = window.document.getElementById("buffer");
    // var bufferBegin = window.document.getElementById("bufferBegin");
    var bufferEnd = window.document.getElementById("bufferEnd");
    // todo
};

this.autoScroll = function() {
    if (window.pageYOffset >= lastPageYOffset - pageYFudge) {
        window.scrollTo(0, window.document.height);
        pageYFudge = window.pageYOffset + window.innerHeight - window.document.height;
        reviewingMessages = 0;
    } else {
        reviewingMessages = 1;
    }
    lastPageYOffset = window.document.height - window.innerHeight;
};

// command editor

this.setSilent = function(silent2) {
    if (silent != silent2) {
        silent = silent2;
        commandBox.type = silent? "password" : "textbox";
        commandBox.focus();
    }
};


// keypress handler
commandBox.onkeydown = function (event) {
    var key = String.fromCharCode(event.which);
    if (0) {
    } else if (event.which == 13) { // enter
        command();
        return false;
    } else if (event.which == 38) { // up
        commandUp();
        return false;
    } else if (event.which == 40) { // down
        commandDown();
        return false;
    } else if (event.which == 27) { // escape
        this.value = "";
        return false;
    }
    return true;
};

// command history
this.command = function() {
	if (!silent) {
		commandsBefore.push(commandBox.value);
	}
    try {
        handleCommand(commandBox.value, enqueueMessage);
    } catch (x) {
        enqueueException(x);
    }
    commandBox.value = "";
};
this.commandUp = function() {
	if (!silent) {
		if (/[^\s]/.test(commandBox.value)) {
			commandsAfter.unshift(commandBox.value);
		}
		if (commandsBefore.length > 0) {
			commandBox.value = commandsBefore.pop();
		} else {
			commandBox.value = "";
		}
	}
};
this.commandDown = function() {
	if (!silent) {
		if (/[^\s]/.test(commandBox.value)) {
			commandsBefore.push(commandBox.value);
		}
		if (commandsAfter.length > 0) {
			commandBox.value = commandsAfter.shift();
		} else {
			commandBox.value = "";
		}
	}
};

this.handleCommand = function(command, enqueueMessage) {
    var val = eval(command);
    if (val) {
        enqueueMessage("<p>" + val + "</p>");
    }
};

autoScroll();

return this;
})();
