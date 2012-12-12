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
    getArticle = () =>
      article = app.desk.unreadList.get(id)
      article.set('isLoading' : true)
      article.fetch(
        success : (model, response) =>
          app.couch.render(model)
          article.set('isLoading' : false)
        error : (model, err) =>
          console.log err
      )

    if app.desk.unreadList.length > 0 then getArticle()
    else
      app.desk.currListType = 'unread'
      app.desk.unreadList = new UnreadCollection()
      app.desk.render()
      app.desk.unreadList.fetch(
        success : (collection, response, options) ->
          console.log('fetched unread items')
          app.desk.render()
          getArticle()
        error : (collection, err) ->
          console.log(JSON.parse(err.responseText))
      )
  )

  app.render()
  Backbone.history.start()

  window.app = app

  return true
)