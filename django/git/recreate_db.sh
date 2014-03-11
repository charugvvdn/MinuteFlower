#!/bin/sh

echo 'Deleting database...'
rm data.db
echo 'Recreating database...'
python manage.py syncdb --noinput
./seed_db.sh
