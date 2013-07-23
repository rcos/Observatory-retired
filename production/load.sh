sudo -u postgres /usr/bin/createdb observatory -E UTF8 -l en_US.UTF8 -T template0

sudo -u postgres /usr/bin/psql -c "ALTER USER postgres PASSWORD 'zaq12wsxcde34rfv'"

sudo -u postgres psql < /vagrant/production/obs.dump.sql

sudo -u www-data /var/www/Observatory/observatory/manage.py migrate dashboard --noinput

sudo -u www-data /var/www/Observatory/observatory/manage.py migrate todo --fake --noinput

sudo -u www-data rsync /vagrant/production/screenshots/screenshots/* /var/www/Observatory/observatory/media/screenshots/ -vzP
