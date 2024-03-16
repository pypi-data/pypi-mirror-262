# In the name of Allah

from .__DirWatcher import DirWatcher
import typing as T
import os
from .__EZJinja import EZJinja
import threading
import webbrowser
import importlib
import sys
from .__server import StaticServer
import atexit
import time


class Jinjutsu:
    def __init__(
        self, input_package: str = "src", output_path: str = "./build"
    ) -> None:
        print("Source folder path: ", os.path.abspath("./src"))
        self.__input_package_name = input_package
        self.__output_path = output_path
        self.__srcWatcher = None
        self.__liveServerThread = None

        sys.path.append(os.path.join(os.getcwd(), "src"))
        import make

        self.__builderMod = make
        self.__jinj = EZJinja(input_package, self.__output_path)
        self.__jinj.init()

        self.__server = None
        atexit.register(self.__at_exit)

    @property
    def package_name(self) -> str:
        return self.__input_package_name

    @property
    def output_path(self) -> str:
        return os.path.abspath(self.__output_path)

    @property
    def jinj(self) -> EZJinja:
        return self.__jinj

    def build(self):
        print("Building: ", flush=True, end="")
        self.__build()
        print("[Done]", flush=True)

    def __build(self):
        self.__builderMod.run(self.jinj)

    def __reload_source_package(self):
        importlib.reload(self.__builderMod)

    def __srcChangedCBF(self):
        print("Detected change in source folder. Rebuilding: ", flush=True, end="")
        self.__reload_source_package()
        self.__build()
        print("[Rebuild completed]", flush=True)
    
    def __at_exit(self):
        print('@at_exit')
        if self.__server is not None and self.__server.httpd:
            self.__server.httpd.server_close()
            print(f"Server stopped")

    def __liveServerWorker(self, port: int):
        self.__server = StaticServer(self.output_path, port)
        self.__server.serve_forever()
        # os.system(f'live-server {self.output_path} -p {port}')

    def join(
        self, live_server_port: int = 5500, index_url: str = "/index.html", **kwargs
    ):
        if kwargs["build"]:
            print("Jinjutsu: Building...")
            self.build()
            return
        elif kwargs["server"]:
            self.start(live_server_port=live_server_port, index_url=index_url)
        else:
            print(
                "Jinjutsu error. Use either -b to single build or -s to start development server."
            )

    def start(self, live_server_port: int = 5500, index_url: str = "/index.html"):
        print("Staring Jinjutsu server...")
        self.__srcWatcher = DirWatcher(self.__input_package_name, self.__srcChangedCBF)
        self.__liveServerThread = threading.Thread(
            target=self.__liveServerWorker, daemon=True, args=(live_server_port,)
        )
        self.__liveServerThread.start()
        while index_url.startswith("/"):
            index_url = index_url[1:]
        self.__build()
        while self.__server.port is None:
            time.sleep(0.1)
        webbrowser.open(
            f"http://localhost:{self.__server.port}/{index_url}", new=0, autoraise=True
        )
        print(f"\nYou can use the following address:\n\nhttp://localhost:{self.__server.port}/index.html\n\n")
        self.__srcWatcher.join()
