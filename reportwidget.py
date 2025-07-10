#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from PySide6.QtCore import QObject,  Qt
from PySide6.QtWidgets import QWidget,  QLabel,  QHBoxLayout, QVBoxLayout, QComboBox, QPushButton,  QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView

import calendar

from stopwatch import StopWatch
from reportwebpage import ReportWebPage
from reportmanager import ReportManager

class ReportWidget(QWidget, QObject):

    def __init__(self):
        
        super().__init__()
        
        self.watch = StopWatch()
        self.watch.start("init Report Widget")
        
        self.report_manager = ReportManager()
        self.report_view = QWebEngineView()
        self.report_page = ReportWebPage(self.create_report_from_url)
        self.report_view.setPage(self.report_page)
        #self.report_view.page().createStandardContextMenu()
        
        self.control_layout = QHBoxLayout()
        
        ### report typ list
        self.control_typ_label = QLabel("Report type")
        self.control_typ = QComboBox()
        self.control_typ.addItem("Overview")
        self.control_typ.addItem("All time")
        self.control_typ.addItem("Year Report")
        self.control_typ.addItem("Month Report")
        self.control_typ.addItem("Day Report")
        self.control_typ.addItem("Album Report")
        self.control_typ.addItem("Person Report")
        
        self.control_typ.currentIndexChanged.connect(self.update_controls)
        
        ### year list
        self.control_year_label = QLabel("Year")
        self.control_year = QComboBox()

        for a in range(self.report_manager.helper_get_min_year(), self.report_manager.helper_get_max_year() + 1):
                self.control_year.addItem(str(a))

        self.control_year.currentIndexChanged.connect(self.update_days_of_month)
        
        ### month list
        self.control_month_label = QLabel("Month")
        self.control_month = QComboBox()

        self.month_names = ['January',  'February',  'March',  'April',  'May',  'June',  'July',  'August',  'September',  'October',  'November',  'December']

        for a in range(len(self.month_names)):
                self.control_month.addItem(self.month_names[a])

        self.control_month.currentIndexChanged.connect(self.update_days_of_month)
        
        ### day list
        self.control_day_label = QLabel("Day")
        self.control_day = QComboBox()
        
        ### album list
        self.control_album_label = QLabel("Album")
        self.control_album = QComboBox()    
        self.control_album.setFixedWidth(400)
        albums = self.report_manager.helper_get_album_list()

        for a in range(len(albums)):
            self.control_album.addItem(albums[a][0])

        # set the width of the open combolist to the widest element
        self.control_album.view().setMinimumWidth(self.control_album.minimumSizeHint().width())

        self.control_create = QPushButton("Report!")
        self.control_create.clicked.connect(self.create_report)

        self.control_layout.addWidget(self.control_create)
        self.control_layout.addWidget(self.control_typ_label)
        self.control_layout.addWidget(self.control_typ)
        self.control_layout.addWidget(self.control_year_label)
        self.control_layout.addWidget(self.control_year)
        self.control_layout.addWidget(self.control_month_label)
        self.control_layout.addWidget(self.control_month)
        self.control_layout.addWidget(self.control_day_label)
        self.control_layout.addWidget(self.control_day)
        self.control_layout.addWidget(self.control_album_label)
        self.control_layout.addWidget(self.control_album)
        self.control_layout.addStretch()
        
        self.main_layout = QVBoxLayout()

        self.main_layout.addLayout(self.control_layout)
        self.main_layout.addWidget(self.report_view)

        self.setLayout(self.main_layout)

        self.update_controls()
        
        self.create_report()
        
        self.watch.stop("init Report Widget")
    
    def update_days_of_month(self):
         weekday,  days = calendar.monthrange(int(self.control_year.currentText()),  self.control_month.currentIndex() + 1)
         self.control_day.clear()

         for a in range(1,  days + 1):
            self.control_day.addItem(str(a))
            
    def update_controls(self):
        self.control_year_label.hide()
        self.control_year.hide()
        self.control_month_label.hide()
        self.control_month.hide()
        self.control_day_label.hide()
        self.control_day.hide()
        self.control_album_label.hide()
        self.control_album.hide()

        typ = self.control_typ.currentIndex()

        # year report
        if(typ == 2):
            self.control_year_label.show()
            self.control_year.show()

        # month report
        elif(typ == 3):
            self.control_year_label.show()
            self.control_year.show()
            self.control_month_label.show()
            self.control_month.show()

        # day report
        elif(typ == 4):

            self.update_days_of_month()

            self.control_year_label.show()
            self.control_year.show()
            self.control_month_label.show()
            self.control_month.show()
            self.control_day_label.show()
            self.control_day.show()

        # album report
        elif(typ == 5):
            self.control_album_label.show()
            self.control_album.show()
        
    def create_report(self):
        
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        typ = self.control_typ.currentIndex()

        if(typ == 0):
            self.report_view.setHtml(self.report_manager.report_overview())

        elif(typ == 1):
            self.report_view.setHtml(self.report_manager.report_all())
            
        elif(typ == 2):
            self.report_view.setHtml(self.report_manager.report_year(self.control_year.currentText()))
        
        elif(typ == 3):
            self.report_view.setHtml(self.report_manager.report_month(self.control_year.currentText(), self.control_month.currentIndex() + 1))
            
        elif(typ == 4):
            self.report_view.setHtml(self.report_manager.report_day(self.control_year.currentText(), self.control_month.currentIndex() + 1, self.control_day.currentText()))
            
        elif(typ == 5):
            self.report_view.setHtml(self.report_manager.report_album(self.control_album.currentText()))
            
        QApplication.restoreOverrideCursor()
        
    def create_report_from_url(self, url):
        
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        
        print(url.toString())
        print(url.host())
        print(url.path())
        print(url.fragment())

        argument = url.path()[1:]

        if(url.host() == "year"):
            self.report_view.setHtml(self.report_manager.report_year(argument))

        elif(url.host() == "month"):
            self.report_view.setHtml(self.report_manager.report_month(argument[0:4], argument[5:7]))

        elif(url.host() == "day"):
            self.report_view.setHtml(self.report_manager.report_day(argument[0:4], argument[5:7], argument[8:10]))

        elif(url.host() == "album"):
            self.report_view.setHtml(self.report_manager.report_album(argument))
            
        QApplication.restoreOverrideCursor()
        
    def print_report(self):

        self.report_view.pdfPrintingFinished.connect(self.print_finished)
        self.report_view.printToPdf('report.pdf')
        
    def print_finished(self):
        
        print("PDF print finished")
        
    def shutdown(self):
        
        self.report_manager.close_report()
