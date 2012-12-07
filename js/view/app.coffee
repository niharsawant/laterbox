class AppView extends Backbone.View
  initialize : () ->
    _.bindAll(@, 'render')
    @render()

  render : () ->
    readingListTemplate = _.template('
      <ul id="nav-readlist" class="list-horz">
        <li><a id="nav-unread" class="a-launchers nav-readoption <% if(type == "unread") { %>nav-unread-selected<% }%>"
          href="#/unread" data-type="unread" title="">Read Later</a></li>
        <li><a id="nav-scrapbook" class="a-launchers nav-readoption <% if(type == "scrapbook") { %>nav-scrapbook-selected<% }%>"
          href="#/scrapbook" data-type="scrapbook" title="">Scrapbook</a></li>
        <li><a id="nav-archive" class="a-launchers nav-readoption <% if(type == "archive") { %>nav-archive-selected<% }%>"
          href="#/archive" data-type="archive" title="">Archive</a></li>
      </ul>
    ')
    @$('#nav-topbar').html(readingListTemplate(
      'type' : @currListType
    ))
    return true

  currListType : ''

window.AppView = AppView

