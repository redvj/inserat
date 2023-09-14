#!/bin/bash

# Definition von Variablen für das Skript


export MYSQL_PW="pzsjh68sDfV5tmDY3GVs"
MYSQL_SECRET_KEY="iautayynxrpsrzumiautayynxrpsrzum"
MYSQL_DATABASE_URL="mysql+pymysql://admin:$MYSQL_PW@localhost:3306/inserat"
MYSQL_DATABASE_NAME="inserat"
MYSQL_ENV_FILE=".env"


source venv/bin/activate
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done
flask translate compile


# .env-Datei erstellen und Konfigurationen hinzufügen
cat <<EOF > $APP_FOLDER/$MYSQL_ENV_FILE
SECRET_KEY=$MYSQL_SECRET_KEY
DATABASE_URL=$MYSQL_DATABASE_URL
MAIL_USERNAME=inserat.root@gmail.com
MAIL_PASSWORD=iautayynxrpsrzum
MAIL_DEFAULT_SENDER=inserat.root@gmail.com
EOF

exec gunicorn -w 4 --bind 0.0.0.0:5000 wsgi:app