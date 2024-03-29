from concurrent.futures import ThreadPoolExecutor

from celery import Celery
from celery.schedules import crontab

from push.push_config import redis_url

executor = ThreadPoolExecutor(30)

app = Celery(
    __name__,
    broker=redis_url,
    backend=redis_url,
    include=['push.tasks']
)

app.conf.beat_schedule = {
    'update_course': {
        'task': 'push.tasks.update_all_course',
        'schedule': crontab(minute=0, hour=5, day_of_week='0'),
        'args': (),
    },
    'send_course': {
        'task': 'push.tasks.send_course',
        'schedule': crontab(minute='0', hour=7),
        'args': (),
    },
    'clear_today_key': {
        'task': 'push.tasks.clear_today_key',
        'schedule': crontab(minute='10', hour=22),
        'args': (),
    },
    'check_push_status': {
        'task': 'push.tasks.check_push_status',
        'schedule': crontab(minute='15', hour=7),
        'args': (),
    },
}
app.conf.update(
    enable_utc=True,
    timezone='Asia/Shanghai',
)

if __name__ == '__main__':
    app.worker_main()
    # 启动 celery beat
    # celery -A main_push beat -l info

    # 启动 celery worker
    # celery -A main_push worker -l info

    # 启动flower
    # celery -A main_push flower --port=5555
