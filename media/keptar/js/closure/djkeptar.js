
goog.require('goog.dom');
goog.require('goog.events');
goog.require('goog.fx.AnimationQueue');
goog.require('goog.fx.dom.FadeInAndShow');
goog.require('goog.fx.dom.FadeOutAndHide');

goog.provide('djkeptar.init');
goog.provide('djkeptar.showForClick');
goog.provide('djkeptar.showForOver');

/**
 * The configuration object for the djkeptar library
 */
djkeptar.config = djkeptar.config || {};

/**
 * The default time for animations.
 * @type {number}
 */
djkeptar.config.anim_time = djkeptar.config.anim_time || 300;

/**
 * Initialization function for djkeptar
 * @param {number=} opt_time Default animation time (optional).
 */
djkeptar.init = function(opt_time) {
  djkeptar.config.anim_time = opt_time || djkeptar.config.anim_time;

  var elsForClick = goog.dom.getElementsByClass('clickhandle');
  var elsForOver = goog.dom.getElementsByClass('overhandle');
  var elsToHide = goog.dom.getElementsByClass('showforhandle');

  for (var i = 0; i < elsToHide.length; i++) {
    elsToHide[i].style.display = 'none';
  }

  for (var i = 0; i < elsForClick.length; i++) {
    djkeptar.showForClick(elsForClick[i]);
  }

  for (var i = 0; i < elsForOver.length; i++) {
    djkeptar.showForOver(elsForOver[i]);
  }
};

/**
 * Checks if the given c element is the child of p.
 * @param {Object} p The parent element.
 * @param {Object} c The (possible) child element.
 * @return {boolean} Whether c is child of p.
 */
djkeptar.isChildOf = function(p, c) {
  if (c != null) {
    while (c.parentNode) {
      c = c.parentNode;
      if (c == p) {
        return true;
      }
    }
  }
  return false;
};

/**
 * Shows/hides all child elements of 'el' with class 'showforhandle' on
 * mouseover/mouseout events.
 * @param {Object} el The element to bind to.
 * @param {number=} opt_time The time of the animation (optional).
 */
djkeptar.showForOver = function(el, opt_time) {
  var time = opt_time || djkeptar.config.anim_time;

  goog.events.listen(el, 'mouseover', function(e) {
    var children = el.childNodes;
    var queue = new goog.fx.AnimationParallelQueue();
    for (var i = 0; i < children.length; i++) {
      var child = children[i];
      if (child.className && child.className.indexOf('showforhandle') > -1 &&
          child.style && child.style.display == 'none') {
        queue.add(new goog.fx.dom.FadeInAndShow(child, time));
      }
    }
    queue.play();
  });

  goog.events.listen(el, 'mouseout', function(e) {
    var newTarget;
    if (e.toElement) {
      newTarget = e.toElement;
    } else if (e.relatedTarget) {
      newTarget = e.relatedTarget;
    }
    if (djkeptar.isChildOf(el, newTarget)) {
      return;
    }

    var children = el.childNodes;
    var queue = new goog.fx.AnimationParallelQueue();
    for (var i = 0; i < children.length; i++) {
      var child = children[i];
      if (child.className && child.className.indexOf('showforhandle') > -1 &&
          child.style && child.style.display != 'none') {
        queue.add(new goog.fx.dom.FadeOutAndHide(child, time));
      }
    }
    queue.play();
  });
};

/**
 * Shows/hides all siblings of 'el' with class 'showforhandle' on click.
 * @param {Object} el The element to bind to.
 * @param {number=} opt_time The time of the animation (optional).
 */
djkeptar.showForClick = function(el, opt_time) {
  var time = opt_time || djkeptar.config.anim_time;

  goog.events.listen(el, 'click', function(e) {
    var children = el.parentNode.childNodes;
    var queue = new goog.fx.AnimationParallelQueue();
    for (var i = 0; i < children.length; i++) {
      var child = children[i];
      if (child.className && child.className.indexOf('showforhandle') > -1) {
        if (child.style && child.style.display == 'none') {
          queue.add(new goog.fx.dom.FadeInAndShow(child, time));
        } else {
          queue.add(new goog.fx.dom.FadeOutAndHide(child, time));
        }
      }
    }
    queue.play();
  });
};

