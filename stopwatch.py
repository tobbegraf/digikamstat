# #!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time
import inspect

class StopWatch():
    def __init__(self):
        self.starttime = {}
        self.endtime = {}
        return

    def start(self, text):
        text = text
        self.starttime[text] = time.time()
        print("%s: %s start %s" % (inspect.stack()[1].function, text, str(self.starttime[text])))

    def stop(self, text):
        self.endtime[text] = time.time()
        print("%s: %s stop %s" % (inspect.stack()[1].function, text, str(self.endtime[text] - self.starttime[text])))
        self.starttime.pop(text)
        self.endtime.pop(text)
