release: python3 manage.py migrate
web: python3 manage.py collectstatic --noinput && gunicorn upscale.wsgi --log-file 
