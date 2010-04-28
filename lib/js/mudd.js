
// TODO require("global-es5");
// TODO require("packages");

// node
var PROCESS = process;
var SYS = require("sys");
// node-narwhal
var HTTP = require("narwhal/q-http");
var FS = require("narwhal/q-fs");
// narwhal-lib
var Q = require("narwhal/promise-util");
var UTIL = require("narwhal/util");
var HTML = require("html");
// jaque
var ROUTE = require("jaque/route");
// mudd
var world = require("./mudd/world").world;

var port = 8080;
var home = PROCESS.env.PACKAGE_HOME;
var www = FS.join(home, "www");

Q.when(world.start(), function (worldRunner) {
    SYS.puts("World started");

    var app = ROUTE.Decorators(
        [
            ROUTE.Error,
            ROUTE.Log,
            ROUTE.ContentLength
        ],
        ROUTE.ComponentMap(
            {
                "": ROUTE.Redirect("index.html"),
                "world.json": ROUTE.Json(function (request) {
                    return world;
                }),
                "world.text": ROUTE.Inspect(function (request) {
                    return world;
                }),
                "sessions.text": ROUTE.Inspect(function (request) {
                    return sessions;
                }),
                "session": ROUTE.CookieSession(function (cookieSession) {
                    return ROUTE.PathSession(function (pathSession) {
                        var downstream = Q.Buffer();
                        var upstream = Q.Buffer();
                        var connection = world.connect({
                            "send": downstream.put,
                            "receive": upstream.get
                        }, pathSession, cookieSession);
                        return ROUTE.Method({
                            "GET": ROUTE.Json(function (request) {
                                return downstream.flush();
                            }),
                            "POST": function (request) {
                                return Q.when(request.body, function (body) {
                                    return Q.when(body.read(), function (body) {
                                        upstream.put(body);
                                        return {
                                            "status": 200,
                                            "headers": {},
                                            "body": []
                                        };
                                    });
                                });
                            }
                        });
                    });
                })
            },
            // not found...
            ROUTE.Method({"GET": ROUTE.FileTree(www)})
        )
    );

    var server = HTTP.Server(app);

    var siginted;
    PROCESS.addListener("SIGINT", function () {
        if (siginted)
            throw new Error("Force stopped");
        siginted = true;
        worldRunner.stop();
    });

    Q.when(server.listen(port), function () {
        SYS.puts("Listining on " + port);
    });

    return Q.when(worldRunner.stopped, function () {
        SYS.puts("World stopped");
        Q.when(server.stop(), function () {
            SYS.puts("Server stopped");
        });
    });

});

