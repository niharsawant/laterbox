(function() {
  var startRouter;

  startRouter = function() {
    app.router = new AppRouter();
    app.router.on('route:getReadingList', function(action, page) {
      app.currListType = action;
      switch (action) {
        case 'unread':
          app.views.desk.render();
          app.user.get('unreads').fetch({
            success: function(collection, response, options) {
              console.log('fetched unread items');
              return app.views.desk.render();
            },
            error: function(collection, err) {
              return console.log(JSON.parse(err.responseText));
            }
          });
          break;
        default:
          app.views.desk.render();
      }
      app.views.couch.reset();
      return app.views.main.render();
    });
    app.router.on('route:getArticle', function(id) {
      var getArticle,
        _this = this;
      getArticle = function() {
        var article;
        article = app.user.get('unreads').get(id);
        article.set({
          'isLoading': true
        });
        return article.fetch({
          success: function(model, response) {
            app.views.couch.render(model);
            return article.set({
              'isLoading': false
            });
          },
          error: function(model, err) {
            article.set({
              'isLoading': false
            });
            return console.log(JSON.parse(err.responseText));
          }
        });
      };
      if (app.collections.unread) {
        return getArticle();
      } else {
        app.currListType = 'unread';
        app.views.desk.render();
        return app.user.get('unreads').fetch({
          success: function(collection, response, options) {
            console.log('fetched unread items');
            app.views.desk.render();
            return getArticle();
          },
          error: function(collection, err) {
            return console.log(JSON.parse(err.responseText));
          }
        });
      }
    });
    Backbone.history.start();
    if (!Backbone.history.fragment) {
      return Backbone.history.navigate('/#/unread', {
        trigger: true
      });
    }
  };

  $(document).ready(function() {
    window.app = {
      views: {},
      collections: {},
      router: {},
      currListType: null
    };
    app.views.main = new AppView({
      el: $('body')
    });
    app.views.desk = new DeskView({
      el: $('#container')
    });
    app.views.couch = new CouchView({
      el: $('#reader')
    });
    app.views.readPreference = new AppPrefView({
      el: $('#readpref')
    });
    app.user = new User();
    app.user.fetch({
      success: function(model, response) {
        return startRouter();
      },
      error: function(e) {
        return console.error(e);
      }
    });
    app.views.main.render();
    return true;
  });

}).call(this);
