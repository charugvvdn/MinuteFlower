function TJsElement(container) {}

TJsElement.prototype.init = function(container) {
    this.id = uniqid();
    this.container = container;
    this.container.hide();
}

TJsElement.prototype.create = function() {
    this.update();
    this.addListeners();
    this.container.show();
}

TJsElement.prototype.destroy = function() {
    this.container.hide();
}

TJsElement.prototype.update = function() {}

TJsElement.prototype.addListeners = function() {
    this.clearListeners();
}

TJsElement.prototype.clearListeners = function() {}
