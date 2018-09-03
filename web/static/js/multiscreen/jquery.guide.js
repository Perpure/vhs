var currentTop;
var currentHeight;

// Generated by CoffeeScript 1.8.0
(function() {
  (function($) {
    var jQueryGuide;
    $.guide = function(options) {
      var action, guide, _i, _len, _ref;
      guide = new jQueryGuide();
      if (options.actions !== void 0) {
        _ref = options.actions;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          action = _ref[_i];
          guide.addAction(action);
        }
      }
      guide.buildLayout();
      guide.layout.bg.click((function(_this) {
        return function() {
          return guide.next();
        };
      })(this));
      $(window).resize((function(_this) {
        return function() {
          return guide.draw();
        };
      })(this));
      $(window).scroll((function(_this) {
        return function() {
          return guide.draw();
        };
      })(this));
      guide.execAction();
      return guide;
    };
    return jQueryGuide = (function() {
      function jQueryGuide() {
        this.layout = {
          container: '',
          bg: '',
          content: ''
        };
        this.step = {
          current: 0,
          status: 0
        };
        this.actionList = [];
      }

      jQueryGuide.prototype.buildLayout = function() {
        var layout, layoutId;
        layoutId = Math.round(Math.random() * 10000);
        layout = $('<div class="jquery-guide" id="jQueryGuide' + layoutId + '"><div class="jquery-guide-bg"></div><div class="jquery-guide-content"></div></div>');
        $('html>body').append(layout);
        this.layout.container = $('#jQueryGuide' + layoutId);
        this.layout.bg = this.layout.container.find('>.jquery-guide-bg');
        return this.layout.content = this.layout.container.find('>.jquery-guide-content');
      };

      jQueryGuide.prototype.addAction = function(action) {
        if (action.content === void 0) {
          this.action.content = "";
        }
        if (action.offsetX === void 0) {
          action.offsetX = 0;
        }
        if (action.offsetY === void 0) {
          action.offsetY = 0;
        }
        if (action.isBeforeFuncExec === void 0) {
          action.isBeforeFuncExec = false;
        }
        return this.actionList.push(action);
      };

      jQueryGuide.prototype.execAction = function() {
        var action;
        action = this.actionList[this.step.current];
        if (this.step.status === 0) {
          this.step.status = 1;
          if (action.beforeFunc !== void 0) {
            action.beforeFunc(this);
          }
          if (action.isBeforeFuncExec) {
            return;
          }
        }
        this.step.status = 2;
        this.animate();
        if (action.successFunc !== void 0) {
          this.step.status = 3;
          return action.successFunc(this);
        }
      };

      jQueryGuide.prototype.back = function() {
        if (his.step.current === 0) {
          this.exit();
          return false;
        }
        this.step = {
          current: --this.step.current,
          status: 0
        };
        this.execAction();
        return true;
      };

      jQueryGuide.prototype.next = function() {
        if (this.step.current + 1 === this.actionList.length) {
          this.exit();
          return false;
        }
        this.step = {
          current: ++this.step.current,
          status: 0
        };
        this.execAction();
        return true;
      };

      jQueryGuide.prototype.exit = function() {
        return this.layout.container.remove();
      };

      jQueryGuide.prototype.animate = function() {
        var action, bgBottomWidth, bgScrollTop, bgTopWidth, scrollTop;
        action = this.actionList[this.step.current];
        scrollTop = $(window).scrollTop();
        bgScrollTop = action.element.offset().top - scrollTop;
        bgTopWidth = bgScrollTop > 0 ? bgScrollTop : 0;
        bgBottomWidth = (bgScrollTop + action.element.innerHeight()) > 0 ? $(window).innerHeight() - (action.element.innerHeight() + bgScrollTop) : $(window).innerHeight();
        currentTop = action.element.offset().top - 7;
        currentHeight = action.element.height() + 14;
        return this.layout.bg.animate({
          width: action.element.innerWidth(),
          height: action.element.innerHeight() + (bgScrollTop < 0 ? bgScrollTop : 0),
          borderTopWidth: bgTopWidth,
          borderRightWidth: $(window).innerWidth() - action.element.offset().left - action.element.innerWidth() + 1,
          borderBottomWidth: bgBottomWidth,
          borderLeftWidth: action.element.offset().left
        }, (function(_this) {
          return function() {
            _this.layout.content.html(action.content);
          };
        })(this));
      };

      jQueryGuide.prototype.draw = function() {
        var action, bgBottomWidth, bgScrollTop, bgTopWidth, scrollTop;
        action = this.actionList[this.step.current];
        scrollTop = $(window).scrollTop();
        bgScrollTop = action.element.offset().top - scrollTop;
        bgTopWidth = bgScrollTop > 0 ? bgScrollTop : 0;
        bgBottomWidth = (bgScrollTop + action.element.innerHeight()) > 0 ? $(window).innerHeight() - (action.element.innerHeight() + bgScrollTop) : $(window).innerHeight();
        this.layout.bg.css({
          width: action.element.innerWidth(),
          height: action.element.innerHeight() + (bgScrollTop < 0 ? bgScrollTop : 0),
          borderTopWidth: bgTopWidth,
          borderRightWidth: $(window).innerWidth() - action.element.offset().left - action.element.innerWidth(),
          borderBottomWidth: bgBottomWidth,
          borderLeftWidth: action.element.offset().left
        });
      };

      return jQueryGuide;

    })();
  })(jQuery);

}).call(this);
