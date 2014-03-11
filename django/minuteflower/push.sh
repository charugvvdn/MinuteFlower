#!/bin/sh

cd /home/minuteflower/webapps/django/git
#git pull
cd /home/minuteflower/webapps/static/
rm -rf img css js
cp /home/minuteflower/webapps/django/git/static/* -r .
cd /home/minuteflower/webapps/django/minuteflower
rm -rf *
cp ../git/* -r .
cp webfaction/* .
../apache2/bin/restart
chmod +x push.sh
