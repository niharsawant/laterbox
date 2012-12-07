$(document).ready(() ->
  app = new AppView(el : $ 'body')
  desk = new DeskView(el : $ '#desk')

  app_router = new AppRouter()
  app_router.on('route:getReadingList', (action, page) ->
    app.currListType = action
    if action is 'unread'
      unreadList = new UnreadCollection()
      desk.unreadList = unreadList
      unreadList.fetch(
        success : (collection, response, options) ->
          console.log('fetched unread items')
          desk.render()
        error : (collection, err) ->
          console.log(JSON.parse(err.responseText))
      )
    app.render()
  )

  Backbone.history.start()

  return true
)