#!/usr/bin/env bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source "${HOME}/.local/bin/env"
DATABASE_URL=$(grep -E '^DATABASE_URL=' .env | cut -d '=' -f2-)
make install && psql -a -d "${DATABASE_URL//+psycopg/}" -f database.sql
