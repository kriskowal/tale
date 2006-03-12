window.messageBuffer = (function () {

// title
this.titleBase = "Tale";
this.hasFocus = 0;
this.reviewingMessages = 0;

// messages
this.unviewedMessageCount = 0;
this.messageCountMax = 64;
this.pageYFudge = 10;
this.lastPageYOffset = 0;

// commands
this.silent = 0;
this.commandsBefore = [];
this.commandsAfter = [];

// title

this.refreshTitle = function () {
    if ((!hasFocus || reviewingMessages) && unviewedMessageCount > 0) {
        this.title = "[" + unviewedMessageCount + "] " + titleBase;
    } else {
        this.title = this.titleBase;
        unviewedMessageCount = 0;
    }
};

this.setTitle = function(newTitle) {
    this.titleBase = newTitle;
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
        document.getElementById("command").focus();
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
			enqueueMessage("<pre>Unable to load: " + url + "</pre>");
		}
		
	} catch (x) {

		enqueueMessage(
            "<p><b>Exception:</b><p>" +
            x +
            "</p><p>Unable to load <tt>" +
            url + 
            "</tt>"
        );

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

// prompt

this.setPrompt = function(message) {
	var prompt = document.getElementById("prompt");
	prompt.value = message;
};


// command editor

this.setSilent = function(silent) {
	var command = document.getElementById("command");
	command.type = silent? "password" : "";
};


// keypress handler
document.getElementById("command").onkeydown = function (event) {
    var key = String.fromCharCode(event.which);
    if (0) {
    } else if (event.which == 13) { // enter
        command(this);
        return false;
    } else if (event.which == 38) { // up
        commandUp(this);
        return false;
    } else if (event.which == 40) { // down
        commandDown(this);
        return false;
    } else if (event.which == 27) { // escape
        this.value = "";
        return false;
    }
    return true;
};

// command history
this.command = function(command) {
	if (!silent) {
		commandsBefore.push(command.value);
	}
    try {
        handleCommand(command.value, enqueueMessage);
    } catch (x) {
        enqueueMessage("<p><b>Exception:</b> <tt>" + x + "</tt></p>");
    }
    command.value = "";
};
this.commandUp = function(command) {
	if (!silent) {
		if (/[^\s]/.test(command.value)) {
			commandsAfter.unshift(command.value);
		}
		if (this.commandsBefore.length > 0) {
			command.value = commandsBefore.pop();
		} else {
			command.value = "";
		}
	}
};
this.commandDown = function(command) {
	if (!silent) {
		if (/[^\s]/.test(command.value)) {
			commandsBefore.push(command.value);
		}
		if (commandsAfter.length > 0) {
			command.value = commandsAfter.shift();
		} else {
			command.value = "";
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

