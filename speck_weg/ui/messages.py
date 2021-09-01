# fingertraining
# Stefan Hochuli, 01.09.2021,
# Folder: speck_weg/ui File: messages.py
#

from PyQt5.QtWidgets import QMessageBox, QPushButton


def open_message_box(title: str, text: str, level: str, informative_text: str = None,
                     button_accept_name: str = None, button_reject_name: str = None):
    """
    :param title:
    :param text:
    :param level:
    :param informative_text:
    :param button_accept_name:
    :param button_reject_name:
    :return: True -> button_accept clicked; False -> button_reject_clicked
    """

    msg = QMessageBox()
    if level == 'information':
        msg.setIcon(QMessageBox.Information)
    elif level == 'question':
        msg.setIcon(QMessageBox.Question)
    elif level == 'warning':
        msg.setIcon(QMessageBox.Warning)
    elif level == 'critical':
        msg.setIcon(QMessageBox.Critical)
    else:
        raise ValueError(
            "level must be one of 'information', 'question', 'warning' or 'critical'."
        )

    msg.setWindowTitle(title)
    msg.setText(text)
    if informative_text:
        msg.setInformativeText(informative_text)

    if button_accept_name:
        msg.addButton(QPushButton(button_accept_name), QMessageBox.AcceptRole)
        if not button_reject_name:
            button_reject_name = 'Abbrechen'
        msg.addButton(QPushButton(button_reject_name), QMessageBox.RejectRole)
    else:
        # default: only a OK (Yes button to close
        msg.setStandardButtons(QMessageBox.Ok)

    ret = msg.exec()
    accept = None
    if ret == msg.AcceptRole:
        accept = True
    elif ret == msg.Ok:
        # Default with the OK button
        pass
    elif ret == msg.RejectRole:
        print('rejected')
        accept = False

    return accept
