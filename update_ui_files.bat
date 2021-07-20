:: generate python files
@ECHO OFF
:: activate venv
ECHO activating
cd /d %~dp0
venv\Scripts\activate
:: main window
::pyuic5 -o ui/main_window_ui.py ui/main_window.ui
:: new training program
::pyuic5 -o ui/new_training_program.py ui/new_training_program.ui

PAUSE
