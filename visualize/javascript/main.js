let setupCalendar = ((deepData) => {
  let { DateTime } = luxon;
  let start = DateTime.local().startOf('month');
  let end = DateTime.local().endOf('month');
  let today = DateTime.local();

  calendar = document.querySelector('.calendar');
  let month = document.createElement('div');
  month.textContent = start.monthLong;
  month.className = 'month';
  calendar.appendChild(month);

  let weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  for (let i=0; i< 7; i++) {
    let weekday = document.createElement('div');
    weekday.textContent = weekdays[i];
    weekday.className = 'weekday';
    calendar.appendChild(weekday);
  }

  let durationFromTime = ((time) => {
    return DateTime.fromFormat(time, 'H:m:s.Su');
  });

  let timeScore = ((time) => {
    if (!time) {
      return '';
    }
    duration = durationFromTime(time);
    if (duration.hour < 2) {
      return 'low';
    } else if (duration.hour < 3) {
      return 'med';
    } else {
      return 'high';
    }
  });

  let createTimeNode = ((time) => {
    let timeNode = document.createElement('div');
    if (time) {
      timeNode.className = 'time';
      let duration = durationFromTime(time);
      timeNode.textContent = duration.toFormat('H:mm');
    }
    return timeNode;
  });

  let createDayNode = ((day) => {
    let dayNode = document.createElement('div');
    dayNode.textContent = start.day;
    return dayNode;
  });

  let weekday = 0;
  while (start <= end || weekday % 7 !== 0) {
    let dayContainer = document.createElement('div');
    dayContainer.className = 'day-container';
    if (weekday % 7 + 1 !== start.weekday || start > end) {
      dayContainer.className += ' empty';
    } else {
      let time = deepData[start.toISODate()];
      dayContainer.appendChild(createTimeNode(time));
      dayContainer.appendChild(createDayNode(start.day));
      dayContainer.className += ` ${timeScore(time)}`;

      if (today.hasSame(start, 'day')) {
        dayContainer.className += ' today';
      }
      start = start.plus({days: 1})
    }
    calendar.appendChild(dayContainer);
    weekday += 1
  }
});

fetch('/data/deep.json').then((response) => response.json()).then((data) => {
  setupCalendar(data);
});
