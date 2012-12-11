class DeskView extends Backbone.View
  initialize : () ->
    @render()

  render : () ->
    $(@el).height($(window).height()-70)

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
    @unreadList.each( (item)=>
      @$('#desk').append(articleTemplate(item.toJSON())) )

  events :
    'click .desk-article' : 'getArticle'

  getArticle : (ev) ->
    id = $(ev.currentTarget).data('id')
    article = @unreadList.get(id)
    console.log article.id
    article.fetch(
      success : (model, response) =>
        app.couch.render(model)
      error : (model, err) =>
        console.log err
    )
  unreadList : []

window.DeskView = DeskView