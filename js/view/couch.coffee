class CouchView extends Backbone.View
  initialize : () -> @reset()

  reset : () ->
    $(document).find('html').removeClass('couch-active')
    $(@el).html('')

  render : (model) ->
    couchTemplate = _.template('
      <div class="reader-container">
      <h3 class="reader-title"><%= title %></h3>
      <div class="reader-content"><%= body %></div>
      </div>
    ')
    $(document).find('html').addClass('couch-active')
    $(@el).html(couchTemplate(model.toJSON()))

window.CouchView = CouchView

