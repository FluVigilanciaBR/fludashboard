#!/bin/bash
FLU_HOME=$(python -c "import fludashboard, os; print(os.path.dirname(fludashboard.__file__))")
NUM_WORKERS=4

WSGI_HOST="0.0.0.0"
WSGI_PORT="8000"
WSGI_BIND="$WSGI_HOST:$WSGI_PORT"
WSGI_APP="fludashboard.app:app"

echo '[II] Creating log folder ...'
mkdir $FLU_HOME/log

FLU_LOG="$FLU_HOME/log/fludashboard.log"

echo '[II] Starting update data ...'
python -c "from fludashboard.app import update_data_before_startup as u; u()"
echo '[II] Starting update data [OK]'

echo '[II] Starting app ...'
gunicorn -w $NUM_WORKERS -b $WSGI_BIND --log-file=$FLU_LOG $WSGI_APP
