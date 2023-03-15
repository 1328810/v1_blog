from datetime import datetime
import pendulum


def date_full(date: str):
    date_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    pendulum.set_locale('zh')
    tz = pendulum.now().tz
    time_difference = pendulum.parse(date_obj.strftime('%Y-%m-%d %H:%M:%S'), tz=tz).diff_for_humans()
    return time_difference


if __name__ == '__main__':
    print(date_full('2023-02-20 22:56:12'))
    print(date_full('2023-02-23 22:56:12'))