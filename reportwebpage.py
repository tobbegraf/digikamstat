#!/usr/bin/env pythonF
# -*- coding: UTF-8 -*-

import PySide6.QtWebEngineCore as QtWebEngineCore
from PySide6.QtWebEngineCore import QWebEnginePage

class ReportWebPage(QWebEnginePage):
    
    def __init__(self,  url_function,  parent=None):
        super().__init__()
        self.url_function = url_function

    def acceptNavigationRequest(self, url,  type,  mainframe):
        
#        print(url)
#        print(type)
#        print(mainframe)
        
        if type == QtWebEngineCore.QWebEnginePage.NavigationTypeLinkClicked:
            self.url_function(url)
            return False
        
        elif type == QtWebEngineCore.QWebEnginePage.NavigationTypeTyped:
            return True
