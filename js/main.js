(function() {

  $(document).ready(function() {
    var app, app_router;
    app = new AppView({
      el: $('body')
    });
    app.desk = new DeskView({
      el: $('#container')
    });
    app.couch = new CouchView({
      el: $('#reader')
    });
    app_router = new AppRouter();
    app_router.on('route:getReadingList', function(action, page) {
      app.desk.currListType = action;
      switch (action) {
        case 'unread':
          app.desk.unreadList = new UnreadCollection();
          app.desk.render();
          app.desk.unreadList.fetch({
            success: function(collection, response, options) {
              console.log('fetched unread items');
              return app.desk.render();
            },
            error: function(collection, err) {
              return console.log(JSON.parse(err.responseText));
            }
          });
          break;
        default:
          app.desk.render();
      }
      app.couch.reset();
      return app.render();
    });
    app_router.on('route:getArticle', function(id) {
      var article,
        _this = this;
      article = app.desk.unreadList.get(id);
      return article.fetch({
        success: function(model, response) {
          return app.couch.render(model);
        },
        error: function(model, err) {
          return console.log(err);
        }
      });
    });
    app.render();
    Backbone.history.start();
    window.app = app;
    return true;
  });

}).call(this);
