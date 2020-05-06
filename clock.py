# APScheduler 讓我們的免費 dyno 在快要睡著的時候自己喚醒自己
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import urllib

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-fri', minute='*/20')
def scheduled_job():
    print('========== APScheduler CRON =========')
    # 利用datetime查詢時間
    print(f'{datetime.datetime.now().ctime()}')
    print('========== APScheduler CRON =========')

    url = "https://maplestory8591.herokuapp.com/"
    conn = urllib.request.urlopen(url)
        
    for key, value in conn.getheaders():
        print(key, value)


sched.start()