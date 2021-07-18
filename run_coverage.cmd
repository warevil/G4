@echo off
echo ******************************************************
echo ** ACTIVATE YOUR ENVIRONMENT BEFORE RUN THIS SCRIPT **
echo ******************************************************
coverage run -m unittest
coverage html
coverage xml
coverage report
pause