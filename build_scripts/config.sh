#!/bin/bash

# Überprüfen, ob das Skript mit sudo-Rechten ausgeführt wird
if [ "$EUID" -ne 0 ]; then
    echo "Bitte führen Sie dieses Skript mit sudo-Rechten aus!"
    echo "Verwendung: sudo ./$0"
    echo "----------------------------------------------------------------"
    exit 1
fi

# Definition von Variablen für das Skript
GIT_REPO="https://github.com/redvj/inserat.git"
APP_FOLDER="/home/$USER/inserat"
MYSQL_USER="admin"
export MYSQL_PW="pzsjh68sDfV5tmDY3GVs"
MYSQL_SECRET_KEY="iautayynxrpsrzumiautayynxrpsrzum"
MYSQL_DATABASE_URL="mysql+pymysql://admin:$MYSQL_PW@localhost:3306/inserat"
MYSQL_DATABASE_NAME="inserat"
MYSQL_ENV_FILE=".env"
GUNICORN_CONFIG="/etc/supervisor/conf.d/inserat.conf"
NGINX_CONFIG="inserat"
NGINX_ACCESS_LOG="inserat_access.log"
NGINX_ERROR_LOG="inserat_error.log"

# Systemaktualisierung und Installation von Abhängigkeiten
apt update && apt install -y python3 python3-venv python3-dev mysql-server supervisor nginx git && apt upgrade -y

# Verzeichnis wechseln und GitHub-Repository klonen
cd /home/$USER
git clone $GIT_REPO $APP_FOLDER

# Virtuelle Umgebung erstellen und aktivieren
cd $APP_FOLDER
python3 -m venv venv
source venv/bin/activate

# Anwendungsabhängigkeiten installieren
pip3 install -r requirements.txt

# Installation von Gunicorn, pymysql und cryptography
pip3 install gunicorn pymysql cryptography

# MySQL-Datenbank konfigurieren
mysql -u root <<MYSQL_SCRIPT
CREATE DATABASE $MYSQL_DATABASE_NAME CHARACTER SET utf8 COLLATE utf8_bin;
CREATE USER '$MYSQL_USER'@'localhost' IDENTIFIED BY '$MYSQL_PW';
GRANT ALL PRIVILEGES ON $MYSQL_DATABASE_NAME.* TO '$MYSQL_USER'@'localhost';
FLUSH PRIVILEGES;
MYSQL_SCRIPT

# .env-Datei erstellen und Konfigurationen hinzufügen
cat <<EOF > $APP_FOLDER/$MYSQL_ENV_FILE
SECRET_KEY=$MYSQL_SECRET_KEY
DATABASE_URL=$MYSQL_DATABASE_URL
MAIL_USERNAME=inserat.root@gmail.com
MAIL_PASSWORD=iautayynxrpsrzum
MAIL_DEFAULT_SENDER=inserat.root@gmail.com
EOF

# Datenbankmigration durchführen
flask db upgrade

# Daten in die Datenbank importieren
mysql -u $MYSQL_USER -p$MYSQL_PW $MYSQL_DATABASE_NAME < $APP_FOLDER/backup.sql

# Gunicorn und Supervisor konfigurieren
touch $GUNICORN_CONFIG
cat <<EOF > $GUNICORN_CONFIG
[program:$NGINX_CONFIG]
command=$APP_FOLDER/venv/bin/gunicorn -b localhost:8000 -w 4 app:app
directory=$APP_FOLDER
user=$USER
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
EOF

# Supervisor neu laden
supervisorctl reload

# SSL-Zertifikate generieren
mkdir $APP_FOLDER/certs
yes "" | openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 -keyout $APP_FOLDER/certs/key.pem -out $APP_FOLDER/certs/cert.pem

# Nginx-Konfiguration erstellen
rm /etc/nginx/sites-enabled/default
cat <<EOF > /etc/nginx/sites-enabled/$NGINX_CONFIG
server {
    listen 80;
    server_name _;

    location / {
        return 301 https://\$host\$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name _;

    ssl_certificate $APP_FOLDER/certs/cert.pem;
    ssl_certificate_key $APP_FOLDER/certs/key.pem;

    access_log /var/log/$NGINX_ACCESS_LOG;
    error_log /var/log/$NGINX_ERROR_LOG;

    location / {
        proxy_pass http://localhost:8000;
        proxy_redirect off;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOF

# Supervisor und Nginx neu starten
supervisorctl reload
systemctl restart nginx

echo "export FLASK_APP=app.py" >> ~/.profile

cp flask_uploads.py /home/inserat/venv/lib/python3.10/site-packages/
