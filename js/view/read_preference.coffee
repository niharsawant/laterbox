class AppPrefView extends Backbone.View
  initialize : () ->

  render : () ->
    prefTemplate = _.template('
      <ul>
        <input id="readpref-url" type="text" name="url" value=""> <br>
        <input id="readpref-submiturl" type="button" name="" value="Submit">
      </ul>
    ')

    $(@el).html(prefTemplate())
    return @

  events :
    'click' : 'onClick'
    'click #readpref-submiturl' : 'onSubmit'

  onClick : (ev) -> ev.stopPropagation()
  # prevents invoking of click of document registred in app view

  onSubmit : (ev) ->
    params = url : @$('#readpref-url').val()
    app.user.get('unreads').create(params,
      success : (model, response) ->
        console.log(model)
    )

  show : () ->
    $(@el).removeClass('readpref-inactive').addClass('readpref-active')
    return @

  hide : () ->
    $(@el).removeClass('readpref-active').addClass('readpref-inactive')
    return @

window.AppPrefView = AppPrefView

