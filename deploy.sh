#!/usr/bin/env bash

set -xeo pipefail

cd spt-webui-frontend
./node_modules/@angular/cli/bin/ng.js build
cd ..

rsync -rv spt-webui-frontend/dist/spt-webui-frontend/browser/* deploy@niklas:/var/www/spt-webui/
rsync -rv spt_webui_backend pyproject.toml uv.lock README.md deploy@niklas:/var/www/spt-webui-backend/
