from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore

def message_box(message, icon=None):
    msg = QMessageBox()
    msg.setText(message)
    
    if icon:
        msg.setIcon(icon)

    msg.setWindowModality(QtCore.Qt.ApplicationModal)
    msg.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
    msg.exec_()

def yes_no_message_box(message, icon=None):
    msg = QMessageBox()
    msg.setText(message)
    
    if icon:
        msg.setIcon(icon)

    msg.setWindowModality(QtCore.Qt.ApplicationModal)
    msg.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    return msg.exec_()