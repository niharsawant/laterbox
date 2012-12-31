class Article extends Backbone.RelationalModel
  defaults :
    id          : null
    title       : ''
    isLoading   : false
    description : ''

  urlRoot : '/article'

  relations : []

  validate : (attributes) ->
    if attributes.url is null then return 'URL can not be empty'

window.Article = Article
