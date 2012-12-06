(function() {

  $(document).ready(function() {
    var app, app_router;
    app = new AppView({
      el: $('body')
    });
    app_router = new AppRouter();
    app_router.on('route:getReadingList', function(action, page) {
      app.currentList = action;
      return app.render();
    });
    Backbone.history.start();
    return true;
  });

}).call(this);
