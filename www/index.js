(function ($) {

    var form, prompt, commandLine;

    function setup() {
        $.get("command.frag.html", function (frag) {
            $(frag).insertAfter($("#buffer"));
            prompt = $("#prompt");
            commandLine = $("#command-line");
            commandLine.focus();
            form = $("#command-form");
            form.submit(function () {
                $.post("broadcast/", encodeURIComponent(commandLine.val()));
                commandLine.val("").focus();
                document.documentElement.style.scrollTop = "100%";
                return false;
            });
            poll();
        });
    }

    function poll() {
        $.get("session/", function (data) {
            if (data !== undefined) {
                before();
                $("#buffer").append("<p>" + data + "</p>");
                after();
            }
            poll();
        });
    }

    var wasBottom = true;
    var tolerance = 10;
    function before() {
        var before = $(document).scrollTop();
        $(document).scrollTop(before + 1);
        var after = $(document).scrollTop();
        wasBottom = before === after;
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
