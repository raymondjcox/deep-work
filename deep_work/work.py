"""Main logic for deep work"""

from datetime import datetime, timedelta
import json
import calendar
import csv
from deep_work import constants

def _timestamp_to_datetime(timestamp):
    return datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')

def _to_iso_date(date):
    return date.strftime('%Y-%m-%d')

def _from_iso_date(st_date):
    return datetime.strptime(st_date, '%Y-%m-%d')

def _csv_reader(file):
    return csv.reader(file, delimiter=',', quotechar='|')

def _csv_writer(file):
    return csv.writer(file, delimiter=',', quotechar='|')

def _prev_op(file):
    file.seek(0)
    last_line = list(_csv_reader(file))[-1]
    return last_line[0].lower()

def _elapsed_time(file, now_time):
    file.seek(0)
    last_line = list(_csv_reader(file))[-1]
    start_time = _timestamp_to_datetime(last_line[1])
    delta_time = now_time - start_time
    return str(delta_time).split(':')

class StartException(Exception):
    """Exception when starting deep work"""
    pass

class StopException(Exception):
    """Exception when stopping deep work"""
    pass

class DeepWork:
    def __init__(self, deep_path, visual_path):
        self.deep_path = deep_path
        self.visual_path = visual_path

    def stop(self):
        """Stops deep work"""
        now_time = datetime.now()
        with open(self.deep_path, 'r') as file:
            prev_op = _prev_op(file)
            if prev_op == constants.STOP:
                raise StartException('Session has not started yet!')
            elapsed_time = _elapsed_time(file, now_time)
        self._writerow([constants.STOP, str(now_time)])
        self.update_visual()
        return now_time, elapsed_time

    def start(self, description=None):
        """Starts deep work"""
        with open(self.deep_path, 'r') as file:
            now_time = datetime.now()
            prev_op = constants.STOP
            prev_op = _prev_op(file)
            if prev_op == constants.START:
                raise StartException('Session already in progress!')
            self._writerow([constants.START, str(now_time), description])
        return now_time

    def clear(self):
        """Clears deep work log"""
        open(self.deep_path, 'w').close()

    def log(self):
        """Pretty prints a deep work log"""
        date_hours = self._build_date_hours_dict()
        result = []
        for date in date_hours:
            weekday_name = calendar.day_name[_from_iso_date(date).weekday()]
            result.append('{:<9} {} : {}'.format(weekday_name, date, date_hours[date]))
        return '\n'.join(result)

    def json(self):
        """Outputs json format of deep work log"""
        date_hours = self._build_date_hours_dict()
        for date in date_hours:
            date_hours[date] = str(date_hours[date])
        return json.dumps(date_hours, indent=4, sort_keys=True)

    def update_visual(self):
        """Ouptuts a json log file at the visual_path"""
        with open(self.visual_path, 'w') as f_out:
            f_out.write(self.json())

    def _writerow(self, row):
        with open(self.deep_path, 'a+') as file:
            _csv_writer(file).writerow(row)

    def _build_date_hours_dict(self):
        date_hours = {}
        with open(self.deep_path, 'r') as file:
            reader = _csv_reader(file)
            start_time = None
            current_date = None
            for row in reader:
                if row[0] == constants.START:
                    start_time = _timestamp_to_datetime(row[1])
                    if current_date is None or _to_iso_date(start_time) != current_date:
                        current_date = _to_iso_date(start_time)
                else:
                    end_time = _timestamp_to_datetime(row[1])
                    delta_time = end_time - start_time
                    # Anything less than 30 minutes is not deep work
                    if delta_time > timedelta(minutes=30):
                        if current_date in date_hours:
                            date_hours[current_date] += delta_time
                        else:
                            date_hours[current_date] = delta_time
        return date_hours
