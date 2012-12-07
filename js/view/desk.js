(function() {
  var DeskView,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  DeskView = (function(_super) {

    __extends(DeskView, _super);

    function DeskView() {
      return DeskView.__super__.constructor.apply(this, arguments);
    }

    DeskView.prototype.initialize = function() {
      return this.render();
    };

    DeskView.prototype.render = function() {
      var articleTemplate,
        _this = this;
      if (this.unreadList.length === 0) {
        return true;
      }
      articleTemplate = _.template('\
      <div class="desk-article">\
        <h3 class="desk-header"><%= title %></h3>\
        <p class="desk-para"><%= description %></p>\
        <div class="desk-pageshadow">\
          <div class="desk-pageshadow-right"></div>\
          <div class="desk-pageshadow-left"></div>\
        </div>\
      </div>\
    ');
      return this.unreadList.each(function(item) {
        return $(_this.el).append(articleTemplate(item.toJSON()));
      });
    };

    DeskView.prototype.unreadList = [];

    return DeskView;

  })(Backbone.View);

  window.DeskView = DeskView;

}).call(this);
