
exports.Queue = function () {
    var self = Object.create(exports.Queue.prototype);
    var messages = [];

    self.get = function () {
    };

    self.ack = function (id) {
    };

    self.put = function (value) {
    };

    return self;
};

