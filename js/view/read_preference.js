(function() {
  var AppPrefView,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  AppPrefView = (function(_super) {

    __extends(AppPrefView, _super);

    function AppPrefView() {
      return AppPrefView.__super__.constructor.apply(this, arguments);
    }

    AppPrefView.prototype.initialize = function() {};

    AppPrefView.prototype.render = function() {
      var prefTemplate;
      prefTemplate = _.template('\
      <ul>\
        <input id="readpref-url" type="text" name="url" value=""> <br>\
        <input id="readpref-submiturl" type="button" name="" value="Submit">\
      </ul>\
    ');
      $(this.el).html(prefTemplate());
      return this;
    };

    AppPrefView.prototype.events = {
      'click': 'onClick',
      'click #readpref-submiturl': 'onSubmit'
    };

    AppPrefView.prototype.onClick = function(ev) {
      return ev.stopPropagation();
    };

    AppPrefView.prototype.onSubmit = function(ev) {
      var params;
      params = {
        url: this.$('#readpref-url').val()
      };
      return app.user.get('unreads').create(params, {
        success: function(model, response) {
          return console.log(model);
        }
      });
    };

    AppPrefView.prototype.show = function() {
      $(this.el).removeClass('readpref-inactive').addClass('readpref-active');
      return this;
    };

    AppPrefView.prototype.hide = function() {
      $(this.el).removeClass('readpref-active').addClass('readpref-inactive');
      return this;
    };

    return AppPrefView;

  })(Backbone.View);

  window.AppPrefView = AppPrefView;

}).call(this);
