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
      var articleTemplate, list,
        _this = this;
      $(this.el).height($(window).height() - 70);
      if (this.currListType === 'unread') {
        list = this.unreadList;
      } else {
        list = null;
      }
      this.$('#desk').empty();
      articleTemplate = _.template('\
      <div class="desk-article">\
        <h3 class="desk-header" data-id="<%= id %>"><%= title %></h3>\
        <p class="desk-para"><%= description %></p>\
        <a href="http://<%=domain%>" class="desk-meta">\
          <img class="desk-favicon"\
            src="http://www.google.com/s2/u/0/favicons?domain=<%= domain%>" />\
            <%= domain %></a>\
        <div class="desk-pageshadow">\
          <div class="desk-pageshadow-right"></div>\
          <div class="desk-pageshadow-left"></div>\
        </div>\
      </div>\
    ');
      if (list) {
        return list.each(function(item) {
          var domain;
          domain = item.get('url').replace('http://', '').replace('https://', '').split(/[/?]/)[0];
          return _this.$('#desk').append(articleTemplate({
            id: item.get('id'),
            title: item.get('title'),
            description: item.get('description'),
            domain: domain
          }));
        });
      }
    };

    DeskView.prototype.events = {
      'click .desk-header': 'getArticle'
    };

    DeskView.prototype.currListType = '';

    DeskView.prototype.getArticle = function(ev) {
      var id;
      id = $(ev.currentTarget).data('id');
      return window.location.href = '/#/article/' + id;
    };

    DeskView.prototype.unreadList = [];

    return DeskView;

  })(Backbone.View);

  window.DeskView = DeskView;

}).call(this);
