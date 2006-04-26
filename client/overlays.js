window.overlays = (function () {

this.update = function(to) {
    var from = document.getElementsByTagName(to.nodeName)[0];
    updateNode(from, to);
};

var updateNode = function (from, to) {
    if (to.nodeType == 1) { /* Element Node */
        var toChild = to.firstChild;
        while (toChild) {
            if (toChild.hasAttribute('id')) {
                var fromChild = document.getElementById(toChild.getAttribute('id'));
                if (fromChild) {
                    updateNode(fromChild, toChild);
                } else {
                    toChild = cloneNode(toChild, true);
                    if (toChild.hasAttribute('insertBefore')) {
                        var before = document.getElementById(toChild.getAttribute('insertBefore'));
                        from.insertBefore(toChild, before);
                    } else if (toChild.hasAttribute('insertAfter')) {
                        var after = document.getElementById(toChild.getAttribute('insertAfter'));
                        from.insertAfter(toChild, after);
                    } else {
                        from.insertBefore(toChild, null);
                    }
                }
            } else {
                toChild = cloneNode(toChild, true);
                if (from.firstChild) {
                    from.replaceChild(toChild, from.firstChild);
                } else {
                    from.insertBefore(toChild, null);
                }
            }
            toChild = toChild.nextSibling;
        }
    } else if (to.nodeType == 3) { /* Text Node */
        from.innerHTML = to.data;
    }
};

var cloneNode = window.domSupplement.cloneNode;

return this;
})();
