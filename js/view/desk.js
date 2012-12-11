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
      $(this.el).height($(window).height() - 70);
      if (this.unreadList.length === 0) {
        return true;
      }
      articleTemplate = _.template('\
      <div class="desk-article" data-id="<%= id %>">\
        <h3 class="desk-header"><%= title %></h3>\
        <p class="desk-para"><%= description %></p>\
        <div class="desk-pageshadow">\
          <div class="desk-pageshadow-right"></div>\
          <div class="desk-pageshadow-left"></div>\
        </div>\
      </div>\
    ');
      return this.unreadList.each(function(item) {
        return _this.$('#desk').append(articleTemplate(item.toJSON()));
      });
    };

    DeskView.prototype.events = {
      'click .desk-article': 'getArticle'
    };

    DeskView.prototype.getArticle = function(ev) {
      var article, id,
        _this = this;
      id = $(ev.currentTarget).data('id');
      article = this.unreadList.get(id);
      console.log(article.id);
      return article.fetch({
        success: function(model, response) {
          return app.couch.render(model);
        },
        error: function(model, err) {
          return console.log(err);
        }
      });
    };

    DeskView.prototype.unreadList = [];

    return DeskView;

  })(Backbone.View);

  window.DeskView = DeskView;

}).call(this);
