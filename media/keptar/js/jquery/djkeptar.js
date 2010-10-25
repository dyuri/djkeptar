
/**
 * The djkeptar namespace
 */
var djkeptar = djkeptar || {};

/**
 * The configuration object for the djkeptar library
 */
djkeptar.config = djkeptar.config || {
  anim_time: 300
};

/**
 * Initialization function for djkeptar
 * @param {Object=} opt_config Configuration options (optional).
 */
djkeptar.init = function(opt_config) {
  $.extend(djkeptar.config, opt_config);

  $('.clickhandle').each(function() {
    djkeptar.showForClick(this);
  });
  $('.overhandle').each(function() {
    djkeptar.showForOver(this);
  });
  $('.showforhandle').each(function() {
    this.style.display = 'none';
  });
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

  $(el).bind('mouseover', function(e) {
    $(el).children('.showforhandle').each(function() {
      $(this).show(time);
    });
  });

  $(el).bind('mouseout', function(e) {
    var newTarget;
    if (e.toElement) {
      newTarget = e.toElement;
    } else if (e.relatedTarget) {
      newTarget = e.relatedTarget;
    }
    if (djkeptar.isChildOf(el, newTarget)) {
      return;
    }

    $(el).children('.showforhandle').each(function() {
      $(this).hide(time);
    });
  });
};

/**
 * Shows/hides all siblings of 'el' with class 'showforhandle' on click.
 * @param {Object} el The element to bind to.
 * @param {number=} opt_time The time of the animation (optional).
 */
djkeptar.showForClick = function(el, opt_time) {
  var time = opt_time || djkeptar.config.anim_time;

  $(el).bind('click', function(e) {
    $(el).siblings('.showforhandle').each(function() {
      $(this).toggle(time);
    });
  });
};

