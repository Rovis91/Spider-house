# celery.py

import os
from celery import Celery
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Celery configuration using environment variables
app = Celery('real_estate_scraper')

app.conf.update(
    broker_url=os.getenv('CELERY_BROKER_URL'),
    result_backend=os.getenv('CELERY_RESULT_BACKEND'),
    task_serializer=os.getenv('CELERY_TASK_SERIALIZER', 'json'),
    result_serializer=os.getenv('CELERY_RESULT_SERIALIZER', 'json'),
    accept_content=[os.getenv('CELERY_ACCEPT_CONTENT', 'json')],
    timezone=os.getenv('CELERY_TIMEZONE', 'UTC'),
    enable_utc=os.getenv('CELERY_ENABLE_UTC', 'True').lower() in ['true', '1', 'yes'],
)
