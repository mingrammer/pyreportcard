#!/usr/bin/env bash

# Global vars
PROJ_TEMPLATE_PATH=/tmp/project_name
DJANGO_PROJECT_DIR=/opt/django_project
VIRTUAL_ENV=django_env
DJANGO_PROJECT=my_site
WSGI_RELATIVE_PATH=my_site.py
APACHE_VHOST=django_host
APACHE_SITES_AVAILABLE_DIR=/etc/apache2/sites-available



# clean up from previous provisions
rm -rf $PROJ_TEMPLATE_PATH $DJANGO_PROJECT_DIR
mkdir $PROJ_TEMPLATE_PATH $DJANGO_PROJECT_DIR



# Install OS packages
apt-get update
apt-get install -y apache2 python-pip libapache2-mod-wsgi curl



# Setup a virtualenv
pip install virtualenv
virtualenv $DJANGO_PROJECT_DIR/$VIRTUAL_ENV
$DJANGO_PROJECT_DIR/$VIRTUAL_ENV/bin/pip install django



# Create Django project from template
curl https://github.com/wonwoowon/simpleDjango/blob/master/project_name.py > $PROJ_TEMPLATE_PATH/project_name.py
cd $DJANGO_PROJECT_DIR
$DJANGO_PROJECT_DIR/$VIRTUAL_ENV/bin/django-admin.py startproject $DJANGO_PROJECT --template=$PROJ_TEMPLATE_PATH



# Run the Django dev server
# $DJANGO_PROJECT_DIR/$VIRTUAL_ENV/bin/python $DJANGO_PROJECT/$WSGI_RELATIVE_PATH runserver 0.0.0.0:8080



# Apache HTTP Server config
a2dissite default

# Create a Django virtual host
touch $APACHE_SITES_AVAILABLE_DIR/$APACHE_VHOST

cat <<EOT >> $APACHE_SITES_AVAILABLE_DIR/$APACHE_VHOST
<VirtualHost *:80>
    WSGIDaemonProcess $DJANGO_PROJECT python-path=$DJANGO_PROJECT_DIR/$DJANGO_PROJECT:$DJANGO_PROJECT_DIR/$VIRTUAL_ENV/lib/python2.7/site-packages
    WSGIProcessGroup $DJANGO_PROJECT
    WSGIScriptAlias / $DJANGO_PROJECT_DIR/$DJANGO_PROJECT/$WSGI_RELATIVE_PATH
    ServerAdmin wonwoowon21@gmail.com
    ErrorLog ${APACHE_LOG_DIR}/error.log
    LogLevel warn
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
EOT

# Enable your Django virtual host
a2ensite $APACHE_VHOST
service apache2 restart
