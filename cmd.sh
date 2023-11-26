#!/bin/sh

echo "##############################################"
echo "#               UPDATE APK                   #"
echo "##############################################"
apk update
apk add nodejs npm
echo "##############################################"
echo "#               INSTALL JS                   #"
echo "##############################################"
cd /app/javascript
npm install
npm run build
echo "##############################################"
echo "#             LAUNCH GUNICORN                #"
echo "##############################################"
cd /app
gunicorn index:app --error-logfile "/var/log/gunicorn/error.log" --access-logfile "/var/log/gunicorn/access.log" --capture-output --timeout 90
