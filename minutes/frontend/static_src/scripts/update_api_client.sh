#!/usr/bin/env bash
set -e

DJANGO_SETTINGS_MODULE='minutes_workbench.settings' poetry run django-admin generate_schema > openapi.json
npx openapi-generator generate -g typescript-fetch -o src/api/ -i openapi.json #|| rm openapi.json
