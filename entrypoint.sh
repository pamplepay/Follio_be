#! /bin/bash
echo "* RUN entry_point.sh for GAE"

#echo "********************"
#echo "** COLLECT STATIC **"
#echo "********************"
#python manage.py collectstatic --noinput
#
#echo "*************"
#echo "** MIGRATE **"
#echo "*************"
#python manage.py migrate

echo "** RUN gunicorn"

gunicorn config.wsgi:application \
    --config=gunicorn.config.py \
    --access-logfile=- \
    -b :$PORT

echo "* END entry_point.sh for GAE"
