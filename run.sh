# create tables
python manage.py syncdb --noinput

# create admin account
python manage.py initadmin

# collect static files
python manage.py collectstatic --noinput

# supervisor manages nginx and uwsgi
supervisord -c /etc/supervisord.conf
