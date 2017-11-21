#!/bin/bash
FLU_HOME=$(python -c "from fludashboard import settings as s; print(s.PATH)")
WSGI_BIND="$WSGI_HOST:$WSGI_PORT"
WSGI_APP="fludashboard.app:app"

echo '[II] Updating data ...'
# python -c "from fludashboard.libs.flu_data import update_data_files as upd; upd(True);"

FLU_LOG="$HOME/$WSGI_FLU_LOG"

echo '[II] Starting app ...'
gunicorn -w $WSGI_NUM_WORKERS -b $WSGI_BIND --log-file=$FLU_LOG $WSGI_APP
