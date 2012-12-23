$(document).ready(() ->
  window.app =
    views : {}
    collections : {}
    router : {}
    currListType : null

  app.views.main = new AppView(el : $ 'body')
  app.views.desk = new DeskView(el : $ '#container')
  app.views.couch = new CouchView(el : $ '#reader')

  app.router = new AppRouter()

  app.router.on('route:getReadingList', (action, page) ->
    app.currListType = action
    switch action
      when 'unread'
        app.collections.unread = new UnreadCollection()
        app.views.desk.render()
        app.collections.unread.fetch(
          success : (collection, response, options) ->
            console.log('fetched unread items')
            app.views.desk.render()
          error : (collection, err) ->
            console.log(JSON.parse(err.responseText))
        )
      else
        app.views.desk.render()

    app.views.couch.reset()
    app.views.main.render()
  )
  app.router.on('route:getArticle', (id) ->
    getArticle = () =>
      article = app.collections.unread.get(id)
      article.set('isLoading' : true)
      article.fetch(
        success : (model, response) =>
          app.views.couch.render(model)
          article.set('isLoading' : false)
        error : (model, err) =>
          article.set('isLoading' : false)
          console.log(JSON.parse(err.responseText))
      )

    if app.collections.unread then getArticle()
    else
      app.currListType = 'unread'
      app.collections.unread = new UnreadCollection()
      app.views.desk.render()
      app.collections.unread.fetch(
        success : (collection, response, options) ->
          console.log('fetched unread items')
          app.views.desk.render()
          getArticle()
        error : (collection, err) ->
          console.log(JSON.parse(err.responseText))
      )
  )

  app.views.main.render()
  Backbone.history.start()

  return true
)