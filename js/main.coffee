$(document).ready(() ->
  app = new AppView(el : $ 'body')

  app_router = new AppRouter()
  app_router.on('route:getReadingList', (action, page) ->
    app.currentList = action
    app.render()
  )

  Backbone.history.start()

  return true
)