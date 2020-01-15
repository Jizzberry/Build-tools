@echo on
tasklist /FI "IMAGENAME eq celery.exe" 2>NUL | find /I /N "celery.exe">NUL
if "%ERRORLEVEL%"=="0" taskkill /f /im celery.exe
celery -A Base worker -l info -P gevent