#!/usr/bin/env bash

set -xeo pipefail

cd spt-webui-frontend
ng build
cd ..

rsync -r spt-webui-frontend/dist/spt-webui-frontend/browser/* deploy@niklas:/var/www/spt-webui/

rsync alembic.ini deploy@niklas:/var/www/spt-webui-backend/
rsync README.md deploy@niklas:/var/www/spt-webui-backend/
rsync poetry.lock deploy@niklas:/var/www/spt-webui-backend/
rsync pyproject.toml deploy@niklas:/var/www/spt-webui-backend/
rsync -r alembic pyproject.toml deploy@niklas:/var/www/spt-webui-backend/
rsync -r spt_webui_backend deploy@niklas:/var/www/spt-webui-backend/
