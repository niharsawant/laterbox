class DeskView extends Backbone.View
  initialize : () ->
    @render()

  render : () ->
    $(@el).height($(window).height()-70)

    if @currListType is 'unread' then list = @unreadList
    else list = null

    @$('#desk').empty()

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

    if list then list.each((item) =>
      @$('#desk').append(articleTemplate(item.toJSON())) )

  events :
    'click .desk-article' : 'getArticle'

  currListType : ''

  getArticle : (ev) ->
    id = $(ev.currentTarget).data('id')
    window.location.href = '/#/article/'+id

  unreadList : []

window.DeskView = DeskView