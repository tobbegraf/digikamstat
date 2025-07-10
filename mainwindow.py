#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QAction,  QIcon

from stopwatch import StopWatch
from reportwidget import ReportWidget

# Subclass QMainWindow to customize application's main window

class MainWindow(QMainWindow):
    
    def __init__(self):

        super().__init__()
        
        self.watch = StopWatch();
        self.watch.start("create Mainwindow")
        
        self.report_widget = ReportWidget()
        self.setCentralWidget(self.report_widget)
        
        exit_action = QAction(QIcon('icons/exit.png'), 'Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(QCoreApplication.quit)

        print_action = QAction(QIcon('icons/printAction.png'), 'Print', self)
        print_action.setShortcut('Ctrl+P')
        print_action.setStatusTip('Print Report')
        print_action.triggered.connect(self.report_widget.print_report)

        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(print_action)
        file.addAction(exit_action)
        
        self.resize(1200, 900)
        self.setWindowTitle('digikamstat')
        self.statusBar().showMessage('Ready')

        self.watch.stop("create Mainwindow")

    def closeEvent(self, event):

        self.report_widget.shutdown()
        
        print("close")
        event.accept()
        
