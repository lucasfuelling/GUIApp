import math

import mariadb
import datetime
import requests
import businesstimedelta


# LINE notify https://notify-bot.line.me/en/
token = 'PZjW8OKGaNnipxLSyieVpaNiK1q7961sooSBhAQKqmW'


def connect_to_mariadb() -> mariadb.connection:
    conn = mariadb.connect(
        user="root",
        password="Jiou96189618!",
        host="server2",
        port=3306,
        database="production"
    )
    return conn


def line_notify_message(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code


class Model(object):
    _start_time: datetime.time
    _end_time: datetime.time

    def __init__(self):
        self._machine = None
        self._tube = None
        self._qty = None
        self._start_time = datetime.time(0)
        self._end_time = datetime.time(0)
        self._prod_hours = datetime.timedelta(0)
        self._avg_tubes_hour = None
        self._mold_change_time = None
        self._qty_sum = None
        self._order_qty = None
        self._prod_date = datetime.date

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
    def order_qty(self):
        return self._order_qty

    @order_qty.setter
    def order_qty(self, value):
        self._order_qty = value

    @property
    def mold_change_time(self):
        return self._mold_change_time

    @mold_change_time.setter
    def mold_change_time(self, value):
        self._mold_change_time = value

    @property
    def qty(self):
        if self._qty is None:
            self._qty = 0
        return self._qty

    @qty.setter
    def qty(self, value):
        self._qty = value

    @property
    def qty_sum(self):
        if self._qty_sum is None:
            self._qty_sum = 0
        return self._qty_sum

    @qty_sum.setter
    def qty_sum(self, value):
        self._qty_sum = value



    @property
    def start_time(self):
        return self._start_time.strftime('%H:%M')

    @start_time.setter
    def start_time(self, str_start_time: str):
        self._start_time = datetime.time(hour=int(str_start_time[:len(str_start_time)-2]), minute=int(str_start_time[2:]))

    @property
    def end_time(self):
        return self._end_time.strftime('%H:%M')

    @end_time.setter
    def end_time(self, str_end_time):
        self._end_time = datetime.time(hour=int(str_end_time[:len(str_end_time)-2]), minute=int(str_end_time[-2:]))

    @property
    def prod_hours(self):
        return self._prod_hours

    @property
    def avg_tubes_hour(self):
        if self._avg_tubes_hour is None:
            self._avg_tubes_hour = 0
        return self._avg_tubes_hour

    def calc_qty(self):
        conn = connect_to_mariadb()
        cur = conn.cursor()
        sql = f"SELECT qty_sum FROM hydroforming WHERE machine = {self._machine} and in_production = TRUE ORDER BY production_id DESC LIMIT 1"
        cur.execute(sql)
        row = cur.fetchone()
        conn.close()
        for r in row:
            qty_sum_last = r
        if qty_sum_last is None:
            qty_sum_last = 0
        self._qty = self._qty_sum - qty_sum_last

    def calculate_avg_tubes_hour(self):
        print(self._prod_hours.seconds)
        self._avg_tubes_hour = round(self._qty / (self._prod_hours.seconds/3600), 1)

    def calculate_hours(self):
        date = datetime.date(1, 1, 1)
        start_helper = datetime.datetime.combine(date, self._start_time)
        end_helper = datetime.datetime.combine(date, self._end_time)
        time_12_00 = datetime.time(hour=12, minute=00)
        time_13_00 = datetime.time(hour=13, minute=00)
        time_17_30 = datetime.time(hour=17, minute=30)
        lunch_time = datetime.timedelta(hours=1)
        dinner_time = datetime.timedelta(hours=0.5)
        if self._start_time <= time_12_00 and self._end_time >= time_17_30:
            self._prod_hours = end_helper - start_helper - lunch_time - dinner_time
        elif self._start_time >= time_17_30 and self._end_time >= time_17_30:
            self._prod_hours = end_helper - start_helper
        elif self._start_time >= time_13_00 and self._end_time >= time_17_30:
            self._prod_hours = end_helper - start_helper - dinner_time
        elif self._start_time <= time_12_00 and time_13_00 <= self._end_time <= time_17_30:
            self._prod_hours = end_helper - start_helper - lunch_time
        else:
            self._prod_hours = end_helper - start_helper

    def save_input(self):
        conn = connect_to_mariadb()
        cur = conn.cursor()
        todays_date = datetime.datetime.now().strftime("%Y-%m-%d")
        sql = "INSERT INTO hydroforming (machine, tube, qty, qty_sum, prod_date, prod_hours, avg_tubes_hour, start_time, " \
              "end_time, order_qty) VALUES (?,?,?,?,?,?,?,?,?,?) "
        par = (
        self._machine, self._tube, self._qty, self._qty_sum, todays_date, self._prod_hours.seconds/3600, self._avg_tubes_hour, self._start_time,
        self._end_time, self._order_qty)
        cur.execute(sql, par)
        conn.commit()
        conn.close()

    def update_inproduction(self, machine):
        conn = connect_to_mariadb()
        cur = conn.cursor()
        sql = f"UPDATE hydroforming SET in_production = 0 WHERE machine={machine} and in_production = 1"
        cur.execute(sql)
        conn.commit()
        conn.close()

    def save_mold_change(self, machine, tube, mold_change_time, order_qty):
        # set old mold to out of production
        self.update_inproduction(machine)

        # insert new mold
        conn = connect_to_mariadb()
        cur = conn.cursor()
        todays_date = datetime.datetime.now().strftime("%Y-%m-%d")
        sql = "INSERT INTO hydroforming (machine, tube, mold_change_time, prod_date, order_qty, in_production) VALUES (?,?,?,?,?,?)"
        par = (machine, tube, mold_change_time, todays_date, order_qty, True)
        cur.execute(sql, par)
        conn.commit()
        conn.close()

    def set_last_data_entry(self, mc):
        conn = connect_to_mariadb()
        cur = conn.cursor()
        sql = f"SELECT tube, qty_sum, avg_tubes_hour, order_qty, prod_date FROM hydroforming WHERE machine ={mc} and in_production = TRUE ORDER BY production_id DESC LIMIT 1"
        cur.execute(sql)
        row = cur.fetchone()
        conn.close()
        self._tube, self._qty_sum, self._avg_tubes_hour, self._order_qty, self._prod_date = row

    def get_current_production(self, mc):
        conn = connect_to_mariadb()
        cur = conn.cursor()
        sql = f"SELECT prod_date, tube, qty, avg_tubes_hour, mold_change_time FROM hydroforming WHERE machine = {mc} and in_production = TRUE ORDER BY production_id ASC"
        cur.execute(sql)
        row = cur.fetchall()
        conn.close()
        # loop through list of tuples and replace "None" = 0
        for i, r in enumerate(row):
            temp = list(r)
            for j, item in enumerate(r):
                if item == None:
                    temp[j] = 0
            row[i] = tuple(temp)
        return row

    def estimated_time_of_completion(self, mc, include_overhrs) -> datetime.datetime:
        self.set_last_data_entry(mc)
        frac, whole = math.modf((self._order_qty - self._qty_sum)/self._avg_tubes_hour)
        remaining_hours = whole
        remaining_seconds = frac*3600

        # Define a working day
        workday = businesstimedelta.WorkDayRule(
                start_time=datetime.time(8),
                end_time=datetime.time(17),
                working_days=[0,1,2,3,4,5])

        nightshift = businesstimedelta.WorkDayRule(
                start_time=datetime.time(hour=17, minute=30),
                end_time=datetime.time(hour=20, minute=30),
                working_days=[0,1,2,3,4,5])

        # Take out the lunch break
        lunchbreak = businesstimedelta.LunchTimeRule(
            start_time=datetime.time(12),
            end_time=datetime.time(13),
            working_days=[0, 1, 2, 3, 4, 5])

        # Combine the two
        businesshrs = businesstimedelta.Rules([workday, lunchbreak])
        over_hrs = businesstimedelta.Rules([workday, nightshift, lunchbreak])
        time_8_00 = datetime.time(hour=8, minute=00)
        prod_datetime = datetime.datetime.combine(self._prod_date + datetime.timedelta(days=1), time_8_00)
        if include_overhrs:
            result = prod_datetime + businesstimedelta.BusinessTimeDelta(over_hrs, hours=remaining_hours, seconds=remaining_seconds)
        else:
            result = prod_datetime + businesstimedelta.BusinessTimeDelta(businesshrs, hours=remaining_hours, seconds=remaining_seconds)
        return result
