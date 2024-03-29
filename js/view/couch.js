(function() {
  var CouchView,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  CouchView = (function(_super) {

    __extends(CouchView, _super);

    function CouchView() {
      return CouchView.__super__.constructor.apply(this, arguments);
    }

    CouchView.prototype.initialize = function() {
      return this.reset();
    };

    CouchView.prototype.reset = function() {
      return $(document).find('html').removeClass('couch-active');
    };

    CouchView.prototype.render = function(model) {
      var couchTemplate;
      $(this.el).html('');
      couchTemplate = _.template('\
      <div class="reader-container">\
      <h3 class="reader-title"><%= title %></h3>\
      <div class="reader-content"><%= body %></div>\
      </div>\
    ');
      $(document).find('html').addClass('couch-active');
      return $(this.el).html(couchTemplate(model.toJSON()));
    };

    return CouchView;

  })(Backbone.View);

  window.CouchView = CouchView;

}).call(this);
