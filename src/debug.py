from datetime import datetime
from os import write, mkdir

from pygame import time

class DebugMeta(type): 
    """
    metaclass to create log file on program start
    """
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        cls.make_log()


class Debug(metaclass=DebugMeta):
    @classmethod
    def Log(cls, message: str):
        curtime = time.get_ticks()
        with open(cls.logname, "a") as file:
            file.write("(" + str(curtime) + ") " + message + "\n")

    @classmethod
    def make_log(cls):
        try:
            mkdir("debug")
        except FileExistsError:
            pass

        cls.logname = "debug/" + "log." + str(datetime.now()) + ".txt"
        logfile = open(cls.logname, "w")
        logfile.close()
