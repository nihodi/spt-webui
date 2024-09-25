#!/usr/bin/env bash

set -xeo pipefail

cd spt-webui-frontend
ng build
cd ..

rsync -rv spt-webui-frontend/dist/spt-webui-frontend/browser/* deploy@niklas:/var/www/spt-webui/
rsync -rv spt_webui_backend pyproject.toml poetry.lock README.md alembic alembic.ini pyproject.toml deploy@niklas:/var/www/spt-webui-backend/
