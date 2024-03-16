#
# بسم الله الرحمن الرحیم
# اللهم صل علی محمد و آل محمد
# ---------------------------
# Created on Fri Mar 01 2024
#
# Copyright (c) 2024 Abolfazl Danayi
# adanayidet@gmail.com
#


import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Lock, Thread
import typing as T
import time
import traceback


class Handler(FileSystemEventHandler):

    def __init__(self, build_function: T.Callable, *args, **kwargs) -> None:
        super().__init__()
        self.__build_function = build_function
        self.__L = Lock()
        self.__tB = None
        self.__builder = Thread(target=self.__builder_thread, daemon=True)
        self.__builder.start()
        self.__paused = False

    def __builder_thread(self):
        while True:
            with self.__L:
                if self.__tB is None:
                    pass
                elif time.time() - self.__tB > 0.5:
                    try:
                        if not self.__paused:
                            self.__build_function()
                    except:
                        print('Error while bulding... What went wrong: ')
                        traceback.print_exc()
                    self.__tB = None
            time.sleep(0.2)

    def set_paused(self, paused: bool):
        self.__paused = paused

    def on_any_event(self, event):
        with self.__L:
            if event.is_directory:
                return None
            self.__tB = time.time()


class DirWatcher:
    def __init__(self, folder: str, trigger_function: T.Callable):
        self.__folder = folder
        self.observer = Observer()
        self.__build = trigger_function
    
    def __build_cbf(self):
        self.observer.remove_handler_for_watch(self.__handler, self.__watcher)
        self.__build()
        self.observer.add_handler_for_watch(self.__handler, self.__watcher)

    def set_paused(self, paused: bool):
        self.__handler.set_paused(paused)

    def join(self):
        self.__handler = Handler(self.__build_cbf)
        self.__watcher = self.observer.schedule(self.__handler, self.__folder, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("error")

        self.observer.join()
