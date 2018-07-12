@echo off
rem Global scope batch file for mapping epic invocations
for /f %%i in ('python -c "import epic; print(epic.__path__[0])"') do set EPIC_PATH=%%i
python %EPIC_PATH%\__init__.py %*
