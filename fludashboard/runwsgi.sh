#!/bin/bash
DEPLOY_HOME="/tmp/"
NUM_WORKERS=4

WSGI_HOST="0.0.0.0"
WSGI_PORT="8000"
WSGI_BIND="$WSGI_HOST:$WSGI_PORT"
WSGI_APP="fludashboard.app:app"

ERRLOG="$DEPLOY_HOME/fludashboard_error.log"
ACCESS_LOG="$DEPLOY_HOME/logs/wsgi_server.access"

echo '[II] Starting update data ...'
python -c "from fludashboard.app import update_data_before_startup as u; u()"
echo '[II] Starting update data [OK]'

echo '[II] Starting app ...'
gunicorn -w $NUM_WORKERS -b $WSGI_BIND --log-file=$ERRLOG $WSGI_APP
