class AppRouter extends Backbone.Router
  routes :
    'article/:id' : 'getArticle'
    ':list/:page' : 'getReadingList'
    ':list' : 'getReadingList'

window.AppRouter = AppRouter
