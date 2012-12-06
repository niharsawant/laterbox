class AppRouter extends Backbone.Router
  routes :
    ':list/:page' : 'getReadingList'
    ':list' : 'getReadingList'

window.AppRouter = AppRouter
