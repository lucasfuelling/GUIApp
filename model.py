import mariadb
import datetime as dt


def connect_to_mariadb():
    conn = mariadb.connect(
        user="root",
        password="Jiou96189618!",
        host="192.168.1.98",
        port=3306,
        database="production"
    )
    return conn


class Model(object):
    def __init__(self):
        self._machine = None
        self._tube = None
        self._qty = None
        self._start_time = None
        self._end_time = None
        self._prod_hours = None
        self._avg_tubes_hour = None

    @property
    def machine(self):
        return self._machine

    @machine.setter
    def machine(self, value):
        self._machine = value

    @property
    def tube(self):
        return self._tube

    @tube.setter
    def tube(self, value):
        self._tube = value

    @property
    def qty(self):
        return self._qty

    @qty.setter
    def qty(self, value):
        try:
            self._qty = int(value)
        except:
            raise ValueError('Must be Number!')

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, str_start_time):
        self._start_time = int(str_start_time.split(':')[0]) + int(str_start_time.split(':')[1])/60

    @property
    def end_time(self):
        return self._end_time

    @end_time.setter
    def end_time(self, str_end_time):
        self._end_time = int(str_end_time.split(':')[0]) + int(str_end_time.split(':')[1])/60

    @property
    def prod_hours(self):
        return self._prod_hours

    @property
    def avg_tubes_hour(self):
        return self._avg_tubes_hour

    def calculate_avg_tubes_hour(self):
        self._avg_tubes_hour = round(self._qty / self._prod_hours, 1)

    def calculate_hours(self):
        lunch_time = 1
        dinner_time = 0.5
        if self._start_time <= 12 and self._end_time >= 17.5:
            self._prod_hours = self._end_time - self._start_time - lunch_time - dinner_time
        elif self._start_time >= 17.5 and self._end_time >= 17.5:
            self._prod_hours = self._end_time - self._start_time
        elif self._start_time >= 13 and self._end_time >= 17.5:
            self._prod_hours = self._end_time - self._start_time - dinner_time
        elif self._start_time <= 12 and self._end_time >= 13 and self._end_time <= 17.5:
            self._prod_hours = self._end_time - self._start_time - lunch_time
        else:
            self._prod_hours = self._end_time - self._start_time

    def save(self):
        conn = connect_to_mariadb()
        cur = conn.cursor()
        todays_date = dt.datetime.now().strftime("%Y-%m-%d")
        sql = "INSERT INTO hydroforming (machine, tube, qty, prod_date, prod_hours, avg_tubes_hour, start_time, " \
              "end_time) VALUES (?,?,?,?,?,?,?,?) "
        par = (self._machine, self._tube, self._qty, todays_date, self._prod_hours, self._avg_tubes_hour, self._start_time, self._end_time)
        cur.execute(sql, par)
        conn.commit()
        print('saved')
