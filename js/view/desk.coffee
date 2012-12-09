class DeskView extends Backbone.View
  initialize : () ->
    @render()

  render : () ->
    if @unreadList.length is 0 then return true
    articleTemplate = _.template('
      <div class="desk-article" data-id="<%= id %>">
        <h3 class="desk-header"><%= title %></h3>
        <p class="desk-para"><%= description %></p>
        <div class="desk-pageshadow">
          <div class="desk-pageshadow-right"></div>
          <div class="desk-pageshadow-left"></div>
        </div>
      </div>
    ')
    @unreadList.each( (item)=> $(@el).append(articleTemplate(item.toJSON())) )

  events :
    'click .desk-article' : 'getArticle'

  getArticle : (ev) ->
    id = $(ev.currentTarget).data('id')
    article = @unreadList.get(id)
    console.log article.id
    article.fetch(
      success : (model, response) ->
        console.log response
      error : (model, err) ->
        console.log err
    )
  unreadList : []

window.DeskView = DeskView