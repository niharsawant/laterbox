startRouter = () ->
  app.router = new AppRouter()
  app.router.on('route:getReadingList', (action, page) ->
    app.currListType = action
    switch action
      when 'unread'
        app.views.desk.render()
        app.user.get('unreads').fetch(
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
      article = app.user.get('unreads').get(id)
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
      app.views.desk.render()
      app.user.get('unreads').fetch(
        success : (collection, response, options) ->
          console.log('fetched unread items')
          app.views.desk.render()
          getArticle()
        error : (collection, err) ->
          console.log(JSON.parse(err.responseText))
      )
  )
  Backbone.history.start()

  if not Backbone.history.fragment
    Backbone.history.navigate('/#/unread', trigger : true)


$(document).ready(() ->
  window.app =
    views : {}
    collections : {}
    router : {}
    currListType : null

  app.views.main = new AppView(el : $ 'body')
  app.views.desk = new DeskView(el : $ '#container')
  app.views.couch = new CouchView(el : $ '#reader')
  app.views.readPreference = new AppPrefView(el : $ '#readpref')

  app.user = new User()
  app.user.fetch(
    success : (model, response) ->
      startRouter()
    error : (e) ->
      console.error(e)
  )

  app.views.main.render()

  return true
)