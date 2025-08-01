#!/bin/bash

# ساخت و اجرای frontend
docker compose -p fitplan_deploy \
               -f docker-compose.yml up -d --build
