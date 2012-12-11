class DeskView extends Backbone.View
  initialize : () ->
    @render()

  render : () ->
    $(@el).height($(window).height()-70)

    if @currListType is 'unread' then list = @unreadList
    else list = null

    @$('#desk').empty()

    articleTemplate = _.template('
      <div class="desk-article">
        <h3 class="desk-header" data-id="<%= id %>"><%= title %></h3>
        <p class="desk-para"><%= description %></p>
        <a href="http://<%=domain%>" class="desk-meta">
          <img class="desk-favicon"
            src="http://www.google.com/s2/u/0/favicons?domain=<%= domain%>" />
            <%= domain %></a>
        <div class="desk-pageshadow">
          <div class="desk-pageshadow-right"></div>
          <div class="desk-pageshadow-left"></div>
        </div>
      </div>
    ')

    if list then list.each((item) =>
      domain = item.get('url').replace('http://','').replace('https://','').split(/[/?]/)[0];
      @$('#desk').append(articleTemplate(
        id          : item.get('id')
        title       : item.get('title')
        description : item.get('description')
        domain      : domain
      ))
    )

  events :
    'click .desk-header' : 'getArticle'

  currListType : ''

  getArticle : (ev) ->
    id = $(ev.currentTarget).data('id')
    window.location.href = '/#/article/'+id

  unreadList : []

window.DeskView = DeskView