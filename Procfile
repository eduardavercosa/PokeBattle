web: gunicorn duda.wsgi --chdir backend --limit-request-line 8188 --log-file -
worker: celery worker --workdir backend --app=duda -B --loglevel=info
