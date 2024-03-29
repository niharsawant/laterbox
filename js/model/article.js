(function() {
  var Article,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  Article = (function(_super) {

    __extends(Article, _super);

    function Article() {
      return Article.__super__.constructor.apply(this, arguments);
    }

    Article.prototype.defaults = {
      id: null,
      title: '',
      isLoading: false,
      description: ''
    };

    Article.prototype.urlRoot = '/article';

    Article.prototype.relations = [];

    Article.prototype.validate = function(attributes) {
      if (attributes.url === null) {
        return 'URL can not be empty';
      }
    };

    return Article;

  })(Backbone.RelationalModel);

  window.Article = Article;

}).call(this);
