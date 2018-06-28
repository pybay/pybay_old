!function($) {
  var parentClass = 'sch-schedule';
  var filterEnabledClass = 'sch-schedule-filtered';
  var prefix = 'sch-schedule-filter-';
  $('.sch-filter-list').click(function(e) {
      var target = $(e.target);
      var filter = target.closest('li').data('filter');
      if (filter === undefined) return;
      var schedule = target.closest('.' + parentClass);
      var alreadySelected = schedule.data('filter') === filter;
      if (alreadySelected) {
        filter = '';
      }
      schedule.data('filter', filter);
      schedule.removeClass();
      schedule.addClass(parentClass);
      if (filter) {
        schedule.addClass(filterEnabledClass + ' ' + prefix + filter);
      }
  });
}(jQuery);
