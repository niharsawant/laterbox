$(document).ready(() ->
  app = new AppView(el : $ 'body')
  app.desk = new DeskView(el : $ '#container')
  app.couch = new CouchView(el : $ '#reader')

  app_router = new AppRouter()
  app_router.on('route:getReadingList', (action, page) ->
    app.desk.currListType = action
    switch action
      when 'unread'
        app.desk.unreadList = new UnreadCollection()
        app.desk.render()
        app.desk.unreadList.fetch(
          success : (collection, response, options) ->
            console.log('fetched unread items')
            app.desk.render()
          error : (collection, err) ->
            console.log(JSON.parse(err.responseText))
        )
      else
        app.desk.render()

    app.couch.reset()
    app.render()
  )
  app_router.on('route:getArticle', (id) ->
    article = app.desk.unreadList.get(id)
    article.fetch(
      success : (model, response) =>
        app.couch.render(model)
      error : (model, err) =>
        console.log err
    )
  )

  app.render()
  Backbone.history.start()

  window.app = app

  return true
)