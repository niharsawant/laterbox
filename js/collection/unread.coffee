class UnreadCollection extends Backbone.Collection
  model : Article
  url : '/read'

window.UnreadCollection = UnreadCollection