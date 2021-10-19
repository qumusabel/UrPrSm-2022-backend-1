#!/bin/sh

SQLITE_DB="/tmp/db.sqlite"
exec uvicorn app.server:app --host 0.0.0.0 --port 80

