
var Q = require("narwhal/promise-util");
var EL = require("narwhal/event-loop");
var UTIL = require("narwhal/util");
var Cache = require("chiron/cache").Cache;
var CHIRON = require("chiron");

var world = exports.world = {
};

world.tick = function () {
};

world.start = function () {
    var world = this;
    var running = true;
    var stopping = Q.defer();
    function run() {
        if (running) {
            world.tick();
            EL.setTimeout(run, 1000);
        }
    }
    Q.enqueue(run);
    return {
        "stop": function () {
            running = false;
            stopping.resolve();
        },
        "stopped": stopping.promise
    }
};

var Room = function () {
};

var Mob = function () {
};

Mob.prototype.tick = function () {
};

