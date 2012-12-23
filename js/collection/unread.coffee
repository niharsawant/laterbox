class UnreadCollection extends Backbone.Collection
  model : Article
  url : '/read'
  initialize : () ->
    @on('change:isLoading', (model, value) ->
      app.views.desk.setLoadingState(model, value)
    )

window.UnreadCollection = UnreadCollection