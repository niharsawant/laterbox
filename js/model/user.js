(function() {
  var User,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  User = (function(_super) {

    __extends(User, _super);

    function User() {
      return User.__super__.constructor.apply(this, arguments);
    }

    User.prototype.urlRoot = '/getcreds';

    User.prototype.relations = [
      {
        type: Backbone.HasMany,
        key: 'unreads',
        relatedModel: 'Article',
        collectionType: 'UnreadCollection'
      }
    ];

    return User;

  })(Backbone.RelationalModel);

  window.User = User;

}).call(this);
