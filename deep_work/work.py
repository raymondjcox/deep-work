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

def _prev_op(lines):
    if not lines:
        return constants.STOP
    last_line = lines[-1]
    return last_line.split(',')[0].lower()

class StartException(Exception):
    """Exception when starting deep work"""
    pass

class StopException(Exception):
    """Exception when stopping deep work"""
    pass

class DeepWork:
    def __init__(self, deep_path):
        self.deep_path = deep_path

    def stop(self):
        """Stops deep work"""
        with open(self.deep_path, 'a+') as f_out:
            with open(self.deep_path, 'r') as f_in:
                now_time = datetime.now()
                lines = f_in.readlines()
                prev_op = _prev_op(lines)
                if prev_op == constants.STOP:
                    raise StartException('Session has not started yet!')
                last_line = lines[-1]
                start_time = _timestamp_to_datetime(last_line.split(',')[1].replace('\n', ''))
                delta_time = now_time - start_time
                print("Stopped deep working at", str(now_time))
                print("Total elapsed time:", str(delta_time))
                f_out.write(constants.STOP + ',' + str(now_time) + '\n')

    def start(self):
        """Starts deep work"""
        with open(self.deep_path, 'a+') as f_out:
            with open(self.deep_path, 'r') as f_in:
                now_time = datetime.now()
                prev_op = constants.STOP
                lines = f_in.readlines()
                prev_op = _prev_op(lines)
                if prev_op == constants.START:
                    raise StartException('Session already in progress!')
                print("Started deep working at", str(now_time))
                f_out.write(constants.START + ',' + str(now_time) + '\n')

    def clear(self):
        """Clears deep work log"""
        open(self.deep_path, 'w').close()
        print("Deep log cleared!")

    def log(self):
        """Pretty prints a log of deep work"""
        date_hours = self._build_date_hours_dict()
        result = []
        for date in date_hours:
            weekday_name = calendar.day_name[_from_iso_date(date).weekday()]
            result.append('{:<9} {} : {}'.format(weekday_name, date, date_hours[date]))
        return '\n'.join(result)

    def to_json(self):
        """Outputs json format of day hour log"""
        date_hours = self._build_date_hours_dict()
        for date in date_hours:
            date_hours[date] = str(date_hours[date])
        return json.dumps(date_hours)

    def _build_date_hours_dict(self):
        date_hours = {}
        with open(self.deep_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
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
