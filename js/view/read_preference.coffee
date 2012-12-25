class AppPrefView extends Backbone.View
  initialize : () ->

  render : () ->
    prefTemplate = _.template('
      <ul>
        <form action="/add" method="post" accept-charset="utf-8">
          <input type="text" name="url" value=""> <br>
          <input type="submit" name="" value="Submit">
        </form>
      </ul>
    ')

    $(@el).html(prefTemplate())
    return @

  events :
    'click' : 'onClick'

  onClick : (ev) -> ev.stopPropagation()

  show : () ->
    $(@el).removeClass('readpref-inactive').addClass('readpref-active')
    return @

  hide : () ->
    $(@el).removeClass('readpref-active').addClass('readpref-inactive')
    return @

window.AppPrefView = AppPrefView

