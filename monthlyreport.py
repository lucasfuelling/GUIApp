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
        host="192.168.0.11",
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

def get_sum_lastmonth(mc):
    conn = connect_to_mariadb()
    cur = conn.cursor()
    sql = f"SELECT SUM(qty) FROM hydroforming WHERE machine = {mc} AND month(prod_date) < month(curdate()-INTERVAL 1 MONTH) and year(prod_date) = year(curdate())"
    cur.execute(sql)
    row = cur.fetchone()
    conn.close()
    result, = row
    return result

if __name__ == "__main__":
    mc1 = get_sum_lastmonth(1)
    mc2 = get_sum_lastmonth(2)
    today = datetime.date.today()
    first = today.replace(day=1)
    last_month = first - datetime.timedelta(days=1)
    # send line notification
    msg = '\n' + last_month.strftime("%Y") + '年' + last_month.strftime("%m") + '月' + '\n'
    msg = msg + '\n機器1: ' + str(mc1) + '\n'
    msg = msg + '機器2: ' + str(mc2) + '\n'
    msg = msg + '合計: ' + str(mc1+mc2)
    line_notify_message(token, msg)

