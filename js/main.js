(function() {

  $(document).ready(function() {
    var app, app_router, desk;
    app = new AppView({
      el: $('body')
    });
    desk = new DeskView({
      el: $('#container')
    });
    app_router = new AppRouter();
    app_router.on('route:getReadingList', function(action, page) {
      var unreadList;
      app.currListType = action;
      if (action === 'unread') {
        unreadList = new UnreadCollection();
        desk.unreadList = unreadList;
        unreadList.fetch({
          success: function(collection, response, options) {
            console.log('fetched unread items');
            return desk.render();
          },
          error: function(collection, err) {
            return console.log(JSON.parse(err.responseText));
          }
        });
      }
      return app.render();
    });
    Backbone.history.start();
    return true;
  });

}).call(this);
