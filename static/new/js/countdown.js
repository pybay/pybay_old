!function() {
  var offset = 0;
  var countdowns = [];
  var timeout = null;

  var labels = ['days', 'hours', 'minutes', 'seconds'];

  function divmod(a, b) {
    return { div: Math.floor(a / b), mod: a % b };;
  }

  function formatCount(num) {
    if(num < 0) {
      return '00';
    } else if (num < 10) {
      return '0' + num;
    }
    return num.toString();
  }

  function updateCountdown(index) {
    window.setTimeout(updateCountdown.bind(null, index), 1000);
    var element = countdowns[index];
    var countdownTo = element.countdownTo * 1000;
    var now = Date.now();
    var timeLeft = countdownTo - now - offset;

    var days = divmod(timeLeft, 86400000);
    var hours = divmod(days.mod, 3600000);
    var minutes = divmod(hours.mod, 60000);
    var seconds = divmod(minutes.mod, 1000);

    var counts = {
      days: days.div,
      hours: hours.div,
      minutes: minutes.div,
      seconds: seconds.div
    };

    var hadCount = false;
    for (var i = 0; i < labels.length; i++) {
      var label = labels[i];
      if (hadCount || i + 2 >= labels.length || counts[label]) {
        element.elements[label].innerText = formatCount(counts[label]);
        hadCount = true;
      } else {
        element.elements[label + 'Wrapper'].remove();
      }
    }
  }

  window.countdown = function countdown(element) {
    var referenceTime = element.dataset.countdownReference * 1000;
    var now = Date.now();
    if (Math.abs(referenceTime - now) > 300000) {
      offset = now - referenceTime;
    }

    var elements = {};
    for (var i = 0; i < labels.length; i++) {
      var labelText = labels[i];
      var wrapper = document.createElement('div');
      var count = document.createElement('span');
      var label = document.createElement('span');
      wrapper.classList.add('countdown-part');
      count.classList.add('countdown-count');
      label.classList.add('countdown-label');
      label.innerText = labelText;
      wrapper.appendChild(count);
      wrapper.appendChild(label);
      element.appendChild(wrapper);
      elements[labelText] = count;
      elements[labelText + 'Wrapper'] = wrapper;
    }

    countdowns.push({
      element: element,
      countdownTo: element.dataset.countdownDate,
      elements: elements
    });

    updateCountdown(0);
  };
}();
