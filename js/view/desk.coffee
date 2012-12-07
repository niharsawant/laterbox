class DeskView extends Backbone.View
  initialize : () ->
    @render()

  render : () ->
    if @unreadList.length is 0 then return true
    articleTemplate = _.template('
      <div class="desk-article">
        <h3 class="desk-header"><%= title %></h3>
        <p class="desk-para"><%= description %></p>
        <div class="desk-pageshadow">
          <div class="desk-pageshadow-right"></div>
          <div class="desk-pageshadow-left"></div>
        </div>
      </div>
    ')
    @unreadList.each( (item)=> $(@el).append(articleTemplate(item.toJSON())) )

  unreadList : []

window.DeskView = DeskView