$(document).ready(() ->
  app = new AppView(el : $ 'body')
  app.desk = new DeskView(el : $ '#container')
  app.couch = new CouchView(el : $ '#reader')

  app_router = new AppRouter()
  app_router.on('route:getReadingList', (action, page) ->
    app.currListType = action
    if action is 'unread'
      unreadList = new UnreadCollection()
      app.desk.unreadList = unreadList
      unreadList.fetch(
        success : (collection, response, options) ->
          console.log('fetched unread items')
          app.desk.render()
        error : (collection, err) ->
          console.log(JSON.parse(err.responseText))
      )
    app.render()
  )

  Backbone.history.start()
  window.app = app

  return true
)