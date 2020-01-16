@echo off
call py-dist\scripts\env.bat
set status=1
for /F "tokens=3 delims=: " %%H in ('sc query "RabbitMQ" ^| findstr "        STATE"') do (
  if ["%%H"] == ["RUNNING"] (
    set status=0
  )
)
if %status% == 1 (
    echo RabbitMQ not running or not installed
    set /P openLink=Open link to download RabbitMQ [y/n]?:
    if ["%openLink%"] == ["y"] ( start "" https://github.com/rabbitmq/rabbitmq-server/releases/download/v3.8.2/rabbitmq-server-3.8.2.exe )
    pause
) else (
cd app\
IF NOT EXIST ./auth.db ( python manage.pyc migrate && python manage.pyc createsuperuser )

start startCelery.exe

IF  [%1] == [] (
	echo Using default settings 127.0.0.1:8000
	python manage.pyc runserver 
)
	
IF [%2] == [] (
	echo Using default port 8000
	python manage.pyc runserver %1:8000
)

IF NOT [%1] == [] IF NOT [%2] == [] ( python manage.pyc runserver %1:%2 )
)
tasklist /FI "IMAGENAME eq celery.exe" 2>NUL | find /I /N "celery.exe">NUL
if "%ERRORLEVEL%"=="0" taskkill /f /im celery.exe