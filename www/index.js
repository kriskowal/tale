(function ($) {

    var form, prompt, commandLine;

    function setup() {
        $.get("command.frag.html", function (frag) {
            $(frag).insertAfter($("#buffer"));
            $(document).scrollTop($(document).scrollTop() + 1000);
            prompt = $("#prompt");
            commandLine = $("#command-line");
            commandLine.focus();
            form = $("#command-form");
            form.submit(function () {
                $.post(
                    "session/" + sessionId,
                    encodeURIComponent(commandLine.val())
                );
                commandLine.val("").focus();
                return false;
            });
            $.get("session/", function (session) {
                sessionId = JSON.parse(session).id;
                poll();
            });
        });
    }

    var sessionId = "";
    function poll() {
        $.ajax({
            "url": "session/" + sessionId,
            "success": function (data) {
                if (data !== undefined) {
                    var messages = JSON.parse(data);
                    before();
                    $.each(messages, function (i, message) {
                        $("#buffer").append("<p>" + message.message + "</p>");
                    });
                    after();
                }
                poll();
            }
        });
    }

    var wasBottom = true;
    var tolerance = 10;
    function before() {
        var at = $(document).scrollTop();
        $(document).scrollTop(at + 1);
        var below = $(document).scrollTop();
        $(document).scrollTop(at - 1);
        var above = $(document).scrollTop();
        $(document).scrollTop(at);
        wasBottom = at === below && at !== above;
    }

    function after() {
        if (wasBottom) {
            var el = commandLine.get(0);
            if (el.scrollIntoView) {
                el.scrollIntoView();
            } else {
                window.scrollTop = window.scrollHeight - window.clientHeight;
            }
        }
    }

    $(function () {
        $("#play").focus().click(function () {
            $(".menu").remove();
            setup();
            return false;
        })
    });

})(jQuery);
