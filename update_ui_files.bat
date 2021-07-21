:: generate python files for the qt ui
@ECHO Off

:: Current folder
cd /d %~dp0

:: Generate UI classes in python
:: Resources
venv\Scripts\pyrcc5 -o speck_weg\ui\resources_rc.py speck_weg\ui\resources\resources.qrc
:: Main window
venv\Scripts\pyuic5 --from-imports --output speck_weg\ui\main_window_ui.py speck_weg\ui\main_window.ui
:: Dialogs
venv\Scripts\pyuic5 -o speck_weg\ui\dialogs\training_theme_ui.py speck_weg\ui\dialogs\training_theme.ui
venv\Scripts\pyuic5 -o speck_weg\ui\dialogs\training_program_ui.py speck_weg\ui\dialogs\training_program.ui
venv\Scripts\pyuic5 -o speck_weg\ui\dialogs\training_exercise_ui.py speck_weg\ui\dialogs\training_exercise.ui

:: PAUSE
