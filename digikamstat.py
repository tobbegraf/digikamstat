#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from PySide6.QtWidgets import QApplication
from mainwindow import MainWindow

app = QApplication([])

window = MainWindow()
window.show()
app.exec()


#msg_box = QMessageBox()
#msg_box.setText("The Digikam Database 'digikam4.db' could not be found.\nPlease copy the file in the digikamstat script folder.")
#msg_box.setIcon(QMessageBox.Critical)
#msg_box.exec()
