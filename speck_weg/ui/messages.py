# fingertraining
# Stefan Hochuli, 01.09.2021,
# Folder: speck_weg/ui File: messages.py
#

from typing import TYPE_CHECKING
from PyQt5.QtWidgets import QMessageBox, QPushButton

if TYPE_CHECKING:
    from ..app import Message


def create_message_box(message: 'Message') -> 'QMessageBox':
    msg = QMessageBox()
    set_level(msg, message.level)

    msg.setWindowTitle(message.title)
    msg.setText(message.text)
    if message.informative_text:
        msg.setInformativeText(message.informative_text)

    if message.button_accept_name:
        msg.addButton(QPushButton(message.button_accept_name), QMessageBox.AcceptRole)
        if not message.button_reject_name:
            message.button_reject_name = 'Abbrechen'
        msg.addButton(QPushButton(message.button_reject_name), QMessageBox.RejectRole)
    else:
        # default: only a OK (Yes button to close
        msg.setStandardButtons(QMessageBox.Ok)

    return msg


def set_level(msg: 'QMessageBox', level: str):
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


def open_message_box(message: 'Message'):
    msg = create_message_box(message)

    # evaluate the return values
    ret = msg.exec()
    accept = None
    if ret == msg.AcceptRole:
        # Only, if the message has a button_accept_name (creating an accept button)
        accept = True
    elif ret == msg.Ok:
        # Default with the OK button
        pass
    elif ret == msg.RejectRole:
        # Escape, cancel or custom reject button (message.button_reject_name)
        print('rejected')
        accept = False

    return accept
