@echo off
rem Global scope batch file for mapping epic invocations
FOR /F "tokens=*" %%i IN ('python -c "import epic; print(epic.__path__[0])"') do (
    set EPIC_PATH=%%i
)
call python "%EPIC_PATH%/__init__.py" action=%1 root=%2 %*
