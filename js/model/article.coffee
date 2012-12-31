class Article extends Backbone.RelationalModel
  defaults :
    id          : null
    title       : ''
    isLoading   : false
    description : ''

  urlRoot : '/article'

  relations : []

  validate : (attributes) ->
    if attributes.id is null then return 'id can not be null'
    if attributes.url is null then return 'URL can not be empty'

window.Article = Article
