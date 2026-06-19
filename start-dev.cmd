@echo off
REM Запуск backend + frontend одной командой (порты 8000/5173 освобождаются перед стартом).
cd /d "%~dp0frontend"
call npm run dev
