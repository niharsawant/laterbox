class Article extends Backbone.Model
  defaults :
    q : null
    title : ''
    description : ''

  validate : (attributes) ->
    if attributes.q is null then return 'q can not be null'
    if attributes.url is null then return 'URL can not be empty'

window.Article = Article
