class DeskView extends Backbone.View
  initialize : () ->
    @render()

  render : () ->
    if @unreadList.length is 0 then return true
    articleTemplate = _.template('
      <div class="desk-article">
        <h3><%= title %></h3>
        <p><%= description %></p>
      </div>
    ')
    @unreadList.each( (item)=> $(@el).append(articleTemplate(item.toJSON())) )

  unreadList : []

window.DeskView = DeskView