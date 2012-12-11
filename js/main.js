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
      var unreadList;
      app.currListType = action;
      if (action === 'unread') {
        unreadList = new UnreadCollection();
        app.desk.unreadList = unreadList;
        unreadList.fetch({
          success: function(collection, response, options) {
            console.log('fetched unread items');
            return app.desk.render();
          },
          error: function(collection, err) {
            return console.log(JSON.parse(err.responseText));
          }
        });
      }
      return app.render();
    });
    Backbone.history.start();
    window.app = app;
    return true;
  });

}).call(this);
