(function() {
  var AppView,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  AppView = (function(_super) {

    __extends(AppView, _super);

    function AppView() {
      return AppView.__super__.constructor.apply(this, arguments);
    }

    AppView.prototype.initialize = function() {
      return _.bindAll(this, 'render');
    };

    AppView.prototype.render = function() {
      var readingListTemplate;
      readingListTemplate = _.template('\
      <ul id="nav-readlist" class="list-horz">\
        <li><a id="nav-unread" class="a-launchers nav-readoption <% if(type == "unread") { %>nav-unread-selected<% }%>"\
          href="#/unread" data-type="unread" title="">Read Later</a></li>\
        <li><a id="nav-scrapbook" class="a-launchers nav-readoption <% if(type == "scrapbook") { %>nav-scrapbook-selected<% }%>"\
          href="#/scrapbook" data-type="scrapbook" title="">Scrapbook</a></li>\
        <li><a id="nav-archive" class="a-launchers nav-readoption <% if(type == "archive") { %>nav-archive-selected<% }%>"\
          href="#/archive" data-type="archive" title="">Archive</a></li>\
      </ul>\
    ');
      this.$('#nav-topbar').html(readingListTemplate({
        'type': app.currListType
      }));
      return true;
    };

    AppView.prototype.events = {
      'click #curtain': 'onCurtainClick'
    };

    AppView.prototype.views = {};

    AppView.prototype.collections = {};

    AppView.prototype.onCurtainClick = function(ev) {
      return window.location.href = '/#/' + app.currListType;
    };

    return AppView;

  })(Backbone.View);

  window.AppView = AppView;

}).call(this);
