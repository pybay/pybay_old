!function($) {
  var parentClass = 'sch-schedule';
  var filterEnabledClass = 'sch-schedule-filtered';
  var prefix = 'sch-schedule-filter-';
  $('.sch-filter-list').click(function(e) {
      var target = $(e.target);
      var filter = target.closest('li').data('filter');
      if (filter === undefined) return;
      var schedule = target.closest('.' + parentClass);
      var alreadySelected = filter === '' || schedule.hasClass(prefix + filter);
      schedule.removeClass(function(i, cls) { return cls; });
      schedule.addClass(parentClass);
      if (!alreadySelected) {
        schedule.addClass(filterEnabledClass + ' ' + prefix + filter);
      }
  });
}(jQuery);
