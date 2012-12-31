class User extends Backbone.RelationalModel
  urlRoot : '/getcreds'

  relations : [
    type : Backbone.HasMany
    key : 'unreads'
    relatedModel : 'Article'
    collectionType : 'UnreadCollection'
  ]

window.User = User