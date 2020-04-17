@echo off
call ..\py-dist\scripts\env.bat
IF  [%1] == [] IF [%2] == [] (
	echo Using default host 127.0.0.1 and default port 8000
	python launcher.pyc
)

IF  [%1] == [] IF NOT [%2] == [] (
	echo Using default host 127.0.0.1
	python launcher.pyc -p %2
)

IF [%2] == [] IF NOT [%1] == [] (
	echo Using default port 8000
	python launcher.pyc -a %1
)

IF NOT [%1] == [] IF NOT [%2] == [] ( 
	echo using port %2 host %1
	python launcher.pyc -p %2 -a %1 
)
pause