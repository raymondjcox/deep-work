let { DateTime } = luxon;

class Calendar {
  constructor() {
    this.calendarNode = document.querySelector('.calendar');
  }

  clear() {
    let node = this.calendarNode;
    while (node.firstChild) {
      node.removeChild(node.firstChild);
    }
  }

  buildHeader(luxonMonth, deepData) {
    let monthContainer = document.createElement('div');
    monthContainer.className = 'month-container';
    let month = document.createElement('span');
    month.textContent = `${luxonMonth.monthLong} ${luxonMonth.year}`;
    month.className = 'month';
    let next = document.createElement('a');
    next.className = 'next-month';
    next.innerHTML = '&raquo;';
    next.href = '#';
    let prev = document.createElement('a');
    prev.className = 'previous-month';
    prev.innerHTML = '&laquo;';
    prev.href = '#';

    let goNext = (() => {
      this.clear();
      this.render(deepData, luxonMonth.plus({months: 1}));
      next.removeEventListener('click', goNext);
    });

    let goPrev = (() => {
      this.clear();
      this.render(deepData, luxonMonth.plus({months: -1}));
      prev.removeEventListener('click', goPrev);
    });

    next.addEventListener('click', goNext);
    prev.addEventListener('click', goPrev);

    monthContainer.appendChild(prev);
    monthContainer.appendChild(next);
    monthContainer.appendChild(month);
    return monthContainer;
  }

  buildWeekDay(day) {
    let weekday = document.createElement('div');
    weekday.textContent = day;
    weekday.className = 'weekday';
    return weekday;
  }

  buildDayNode(day) {
    let dayNode = document.createElement('div');
    dayNode.textContent = day;
    return dayNode;
  }

  durationFromTime(time) {
    return DateTime.fromFormat(time, 'H:m:s.Su');
  }

  buildTimeNode(time) {
    let timeNode = document.createElement('div');
    if (time) {
      timeNode.className = 'time';
      let duration = this.durationFromTime(time);
      timeNode.textContent = duration.toFormat('H:mm');
    }
    return timeNode;
  }

  timeScore(time) {
    if (!time) {
      return '';
    }
    let duration = this.durationFromTime(time);
    if (duration.hour < 2) {
      return 'low';
    } else if (duration.hour < 3) {
      return 'med';
    } else {
      return 'high';
    }
  }

  render(data, month) {
    let header = this.buildHeader(month, data);
    let calendarNode = this.calendarNode;
    calendarNode.appendChild(header);

    let weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    for (let i = 0; i< 7; i++) {
      calendarNode.appendChild(this.buildWeekDay(weekdays[i]));
    }

    let weekday = 0;
    let today = DateTime.local();
    let start = month.startOf('month');
    let end = month.endOf('month');
    while (start <= end || weekday % 7 !== 0) {
      let dayContainer = document.createElement('div');
      dayContainer.className = 'day-container';
      if (weekday % 7 + 1 !== start.weekday || start > end) {
        dayContainer.className += ' empty';
      } else {
        let time = data[start.toISODate()];
        dayContainer.appendChild(this.buildTimeNode(time));
        dayContainer.appendChild(this.buildDayNode(start.day));
        dayContainer.className += ` ${this.timeScore(time)}`;

        if (today.hasSame(start, 'day')) {
          dayContainer.className += ' today';
        }
        start = start.plus({days: 1});
      }
      calendarNode.appendChild(dayContainer);
      weekday += 1
    }
  }
}

let calendar = new Calendar();
fetch('/data/deep.json').then((response) => response.json()).then((data) => {
  calendar.render(data, DateTime.local());
});
