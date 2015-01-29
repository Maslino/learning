# coding=utf8
from logging import FileHandler
import os
import errno
import datetime


class MidnightRotatingFileHandler(FileHandler):
    def __init__(self, filename):
        self._filename = filename
        self._rotate_at = self._next_rotate_datetime()
        super(MidnightRotatingFileHandler, self).__init__(filename, mode='a')

    @staticmethod
    def _next_rotate_datetime():
        # rotate at midnight
        now = datetime.datetime.now()
        return now.replace(hour=0, minute=0, second=0) + datetime.timedelta(days=1)

    def _open(self):
        today = datetime.datetime.today()
        log_today = "%s.%s" % (self._filename, today.strftime('%Y-%m-%d'))
        try:
            # create the log file atomically
            fd = os.open(log_today, os.O_CREAT | os.O_EXCL)
            # if coming here, the log file was created
            os.close(fd)
        except OSError as e:
            if e.errno != errno.EEXIST:
                # should not happen
                raise
        self.baseFilename = log_today
        return super(MidnightRotatingFileHandler, self)._open()

    def emit(self, record):
        now = datetime.datetime.now()
        if now > self._rotate_at:
            # time to rotate
            self._rotate_at = self._next_rotate_datetime()
            super(MidnightRotatingFileHandler, self).emit(record)
            self.close()
        else:
            super(MidnightRotatingFileHandler, self).emit(record)
