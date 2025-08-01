REM build and run frontend container
docker compose -p fitplan_deploy ^
               -f docker-compose.yml up -d --build