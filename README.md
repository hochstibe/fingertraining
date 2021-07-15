# fingertraining

## Goals

* Keep track of the training
  * Fingerboard
  * Plank
  * Push up
  * Pull up
* Progress reports
  * per exercise
  * per training plan
  * how often

## Activities

* Save a training plan
* Group plans to a training program
* Rate a training (per exercise)
* Do a training (timers)
* Reminder (calendar) -> web application

# Libraries

* sqlalchemy: core or orm, define tables in python -> use 2.0 syntax (introduced in v1.4.0)
  * [official tutorial](https://docs.sqlalchemy.org/en/14/tutorial/)
  * table definitions separately from orm -> better separation
  * table definitions within separately -> full object with all attributes
* alembic for db migrations
* pyqt
  * [tutorial designer](https://realpython.com/qt-designer-python/) [tutorial sql](https://realpython.com/python-pyqt-database/)
  * sql module (try with sqlalchemy first, some tutorials say, qtsql integrates better with the ui)
  * create the ui with the designer
  * generate classes ``pyuic5 -o ui/main_window_ui.py ui/main_window.ui``
  * application in main.py with all signals, etc.