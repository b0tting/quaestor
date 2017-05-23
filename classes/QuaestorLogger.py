from collections import OrderedDict
import logging
import datetime
import time

class QuaestorLogEnty():
    def __init__(self, time, text):
        self.time = time
        self.msg = text

class QuaestorLogHandler(logging.StreamHandler):
    MAX_ENTRIES = 30

    def __init__(self):
        logging.StreamHandler.__init__(self)
        self.last_entries = []

    def emit(self, record):
        msg = self.format(record)
        if len(self.last_entries) > QuaestorLogHandler.MAX_ENTRIES:
            self.last_entries.popitem(last=False)
        self.last_entries.append(QuaestorLogEnty(datetime.datetime.now(), msg))

    def get_last_entries(self):
        return self.last_entries
