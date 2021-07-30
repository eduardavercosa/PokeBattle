web: gunicorn duda.wsgi --chdir backend --limit-request-line 8188 --log-file -
worker: celery worker --app=duda -B --loglevel=info
