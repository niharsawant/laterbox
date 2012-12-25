class AppView extends Backbone.View
  initialize : () ->
    _.bindAll(@, 'render')

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

      <a id="nav-readpref" class="a-launchers nav-preferences">𝌆</a>
    ')
    @$('#nav-topbar').html(readingListTemplate(
      'type' : app.currListType
    ))
    return @

  events:
    'click #curtain' : 'onCurtainClick'
    'click #nav-readpref' : 'launchReadingPreferences'
    'click' : 'hideControls'

  views : {}

  collections : {}

  launchReadingPreferences : (ev) ->
    @$('#nav-readpref').addClass('nav-readpref-selected')
    app.views.readPreference.render().show()
    return false

  hideReadingPreferences : (ev) ->
    @$('#nav-readpref').removeClass('nav-readpref-selected')
    app.views.readPreference.hide()
    return false

  onCurtainClick : (ev) ->
    window.location.href = '/#/' + app.currListType
    return false

  hideControls : (ev) ->
    @hideReadingPreferences(ev)
    return true


window.AppView = AppView

