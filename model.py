import mariadb
import datetime as dt
import requests

# LINE notify https://notify-bot.line.me/en/
token = 'PZjW8OKGaNnipxLSyieVpaNiK1q7961sooSBhAQKqmW'

def connect_to_mariadb() -> mariadb.connection:
    conn = mariadb.connect(
        user="root",
        password="Jiou96189618!",
        host="192.168.1.98",
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
    def __init__(self):
        self._machine = None
        self._tube = None
        self._qty = None
        self._start_time = None
        self._end_time = None
        self._prod_hours = None
        self._avg_tubes_hour = None
        self._mold_change_time = None
        self._qty_sum = None
        self._order_qty = None

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
        return self._start_time

    @start_time.setter
    def start_time(self, str_start_time: str):
        if len(str_start_time) == 4:
            self._start_time = int(str_start_time[:2]) + int(str_start_time[2:]) / 60
        else:
            self._start_time = int(str_start_time[:1]) + int(str_start_time[2:]) / 60

    @property
    def end_time(self):
        return self._end_time

    @end_time.setter
    def end_time(self, str_end_time):
        self._end_time = int(str_end_time[:2]) + int(str_end_time[2:]) / 60

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

    def save_input(self):
        conn = connect_to_mariadb()
        cur = conn.cursor()
        todays_date = dt.datetime.now().strftime("%Y-%m-%d")
        sql = "INSERT INTO hydroforming (machine, tube, qty, qty_sum, prod_date, prod_hours, avg_tubes_hour, start_time, " \
              "end_time, order_qty) VALUES (?,?,?,?,?,?,?,?,?,?) "
        par = (
        self._machine, self._tube, self._qty, self._qty_sum, todays_date, self._prod_hours, self._avg_tubes_hour, self._start_time,
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
        todays_date = dt.datetime.now().strftime("%Y-%m-%d")
        sql = "INSERT INTO hydroforming (machine, tube, mold_change_time, prod_date, order_qty, in_production) VALUES (?,?,?,?,?,?)"
        par = (machine, tube, mold_change_time, todays_date, order_qty, True)
        cur.execute(sql, par)
        conn.commit()
        conn.close()

    def set_last_data_entry(self, mc):
        conn = connect_to_mariadb()
        cur = conn.cursor()
        if mc == '1':
            sql = "SELECT tube, qty_sum, avg_tubes_hour, order_qty FROM hydroforming WHERE machine = 1 and in_production = TRUE ORDER BY production_id DESC LIMIT 1"
        else:
            sql = "SELECT tube, qty_sum, avg_tubes_hour, order_qty FROM hydroforming WHERE machine = 2 and in_production = TRUE ORDER BY production_id DESC LIMIT 1"
        cur.execute(sql)
        row = cur.fetchone()
        conn.close()
        self._tube, self._qty_sum, self._avg_tubes_hour, self._order_qty = row

    def get_current_production(self, mc):
        conn = connect_to_mariadb()
        cur = conn.cursor()
        if mc == '1':
            sql = "SELECT prod_date, tube, qty, avg_tubes_hour, mold_change_time FROM hydroforming WHERE machine = 1 and in_production = TRUE ORDER BY production_id ASC"
        else:
            sql = "SELECT prod_date, tube, qty, avg_tubes_hour, mold_change_time FROM hydroforming WHERE machine = 2 and in_production = TRUE ORDER BY production_id ASC"
        cur.execute(sql)
        row = cur.fetchall()
        conn.close()
        return row