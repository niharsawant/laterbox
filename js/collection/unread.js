(function() {
  var UnreadCollection,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  UnreadCollection = (function(_super) {

    __extends(UnreadCollection, _super);

    function UnreadCollection() {
      return UnreadCollection.__super__.constructor.apply(this, arguments);
    }

    UnreadCollection.prototype.model = Article;

    UnreadCollection.prototype.url = '/read';

    UnreadCollection.prototype.initialize = function() {
      return this.on('change:isLoading', function(model, value) {
        return app.desk.setLoadingState(model, value);
      });
    };

    return UnreadCollection;

  })(Backbone.Collection);

  window.UnreadCollection = UnreadCollection;

}).call(this);
