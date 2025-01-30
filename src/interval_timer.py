import sys
import threading


def set_interval(func, sec=900, *args):
    sys.stdout = sys.__stdout__
    print(f"\n{round(sec/60, None)} minutes until next db hit.")

    def func_wrapper():
        func(*args)
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t
