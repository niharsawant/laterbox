class Article extends Backbone.Model
  defaults :
    id : null
    title : ''
    description : ''

  urlRoot : '/article'

  validate : (attributes) ->
    if attributes.id is null then return 'id can not be null'
    if attributes.url is null then return 'URL can not be empty'

window.Article = Article
