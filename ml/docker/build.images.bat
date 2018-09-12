@echo off

echo Deleting docker image(s), press any key to continue, or ctrl-c to terminate
pause
docker image rm faisalthaheem/lt-rest:1.0

rem delete stale scripts
echo Cleaning "scripts" directory, press any key to continue, or ctrl-c to terminate
pause
cd scripts
del /f /q *.py
cd ..

rem copy the latest scripts
echo Copying latest scripts from jupyter...
copy "..\jupyter\*.py" .\scripts\

rem build docker images
echo Building images...
rem docker build -t faisalthaheem/lt-base:1.0 -f Dockerfile.base .
docker build -t faisalthaheem/lt-base-ubuntu16:1.0 -f Dockerfile.ubuntu16.04.base .
docker build -t faisalthaheem/lt-rest:1.0 -f Dockerfile.rest .

echo Done.