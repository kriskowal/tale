window.domSupplement = (function () {
        
this.cloneNode = function(from) {
    if (from.nodeType == 1) {
        var to = document.createElement(from.nodeName);
        var fromChild = from.firstChild;
        while (fromChild) {
            to.insertBefore(cloneNode(fromChild), null);
            fromChild = fromChild.nextSibling;
        }
        for (var i = 0; i < from.attributes.length; i++) {
            var attribute = from.attributes.item(i);
            to.setAttribute(attribute.nodeName, attribute.nodeValue);
        }
    } else {
        to = from.cloneNode(1);
    }
    return to;
}

return this;
})();
