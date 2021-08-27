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
venv\Scripts\pyuic5 --from-imports -o speck_weg\ui\dialog_training_theme_ui.py speck_weg\ui\dialog_training_theme.ui
venv\Scripts\pyuic5 --from-imports -o speck_weg\ui\dialog_training_program_ui.py speck_weg\ui\dialog_training_program.ui
venv\Scripts\pyuic5 --from-imports -o speck_weg\ui\dialog_training_exercise_ui.py speck_weg\ui\dialog_training_exercise.ui
venv\Scripts\pyuic5 --from-imports -o speck_weg\ui\dialog_training_exercise_load_ui.py speck_weg\ui\dialog_training_exercise_load.ui
venv\Scripts\pyuic5 --from-imports -o speck_weg\ui\dialog_workout_ui.py speck_weg\ui\dialog_workout.ui
venv\Scripts\pyuic5 --from-imports -o speck_weg\ui\dialog_user_ui.py speck_weg\ui\dialog_user.ui

:: PAUSE
