@echo off
title Aurexis Studio Backend Server
echo Установка зависимостей...
pip install -r requirements.txt
echo Запуск сервера...
python server.py
pause
