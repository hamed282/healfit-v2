import os
from celery import Celery
from datetime import timedelta


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A.settings')

celery_app = Celery('A')
celery_app.autodiscover_tasks()

celery_app.conf.broker_url = 'redis://:kiWPps4PuFcPBAgfMgp@localhost:55177/0' # 'amqp://hamed:hamed@localhost:5672' # 'amqp://rabbitmq' # 'amqp://username:password@localhost:7893'
celery_app.conf.result_backend = 'rpc://'
celery_app.conf.task_serializer = 'json'
celery_app.conf.result_serializer = 'pickle'
celery_app.conf.accept_content = ['json', 'pickle']
celery_app.conf.result_expires = timedelta(days=1)
celery_app.conf.task_always_eager = False
celery_app.conf.worker_prefetch_multiplier = 4
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
