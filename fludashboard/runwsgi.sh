#!/bin/bash
FLU_HOME=$(python -c "from fludashboard import settings as s; print(s.APP_PATH)")
NUM_WORKERS=4

WSGI_HOST="0.0.0.0"
WSGI_PORT="8000"
WSGI_BIND="$WSGI_HOST:$WSGI_PORT"
WSGI_APP="fludashboard.app:app"

echo '[II] Creating log folder ...'
mkdir $FLU_HOME/log

echo '[II] Updating data ...'
python -c "from fludashboard.app import update_data_files as upd; upd(True);"

FLU_LOG="$FLU_HOME/log/fludashboard.log"

echo '[II] Starting app ...'
gunicorn -w $NUM_WORKERS -b $WSGI_BIND --log-file=$FLU_LOG $WSGI_APP
