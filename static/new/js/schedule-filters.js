!function($) {
  var parentClass = 'sch-schedule';
  var filterEnabledClass = 'sch-schedule-filtered';
  var prefix = 'sch-schedule-filter-';
  $('.sch-filter-list').click(function(e) {
      var target = $(e.target);
      var filter = target.closest('li').data('filter');
      if (filter === undefined) return;
      var schedule = target.closest('.' + parentClass);
      schedule.data('filter');
      var alreadySelected = filter === '' || schedule.data('filter') === filter;
      schedule.data('filter', filter);
      schedule.removeClass(function(i, cls) { return cls; });
      schedule.addClass(parentClass);
      if (!alreadySelected) {
        var filters = $.map(filter.split(' '), function (f) {
          return prefix + f;
        }).join(' ');
        schedule.addClass(filterEnabledClass + ' ' + filters);
      }
  });
}(jQuery);
