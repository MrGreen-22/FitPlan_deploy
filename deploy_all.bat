@echo off
chcp 65001 >nul

echo 📦 Deploying Backend...
pushd backend\deployment
call deploy.bat
popd

echo 🎨 Deploying Frontend...
pushd frontend\fit-plan
call deploy.bat
popd

echo ✅ All services are up and running!
pause
