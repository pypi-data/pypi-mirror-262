#
# بسم الله الرحمن الرحیم
# اللهم صل علی محمد و آل محمد
# ---------------------------
# Created on Sun Mar 03 2024
#
# Copyright (c) 2024 Abolfazl Danayi
# adanayidet@gmail.com
#


def _init():
    import os
    import shutil
    import sys

    if os.path.exists("./src"):
        print(
            "src folder already exists. Can not re-initialize it. You should delete this folder yourself, if you want to reinit."
        )
    else:
        print("Creating src folder: ", end="", flush=True)
        import shutil

        try:
            shipath = os.path.join(sys._MEIPASS, "pykatana")
            if not os.path.exists(shipath):
                shipath = os.path.join(shipath, "pykatana")
        except:
            shipath = os.path.abspath(
                __file__.replace("run.py", "").replace("__program.py", "")
            )
        shutil.copytree(os.path.join(shipath, "__pykatana_init/src"), "./src")
        os.makedirs("./src/meta", exist_ok=True)
        os.makedirs("./archive", exist_ok=True)
        os.makedirs("./build", exist_ok=True)
        if not os.path.exists("./.gitignore"):
            shutil.copyfile(
                os.path.join(shipath, "__pykatana_init/gitignore"), "./.gitignore"
            )
        print("""[Done]""")


def run_as_program():
    from .engine import Jinjutsu
    import sys
    import os
    import argparse

    ap = argparse.ArgumentParser(
        prog="pykatana: Jinja2 with a sword!",
        usage="pykatana [switches]",
    )
    ap.add_argument("-b", "--build", help="Build", action="store_true")
    ap.add_argument(
        "-s", "--server", help="Run development server", action="store_true"
    )
    ap.add_argument(
        "-i",
        "--init",
        help="Initialize this folder for a pykatana project",
        action="store_true",
    )
    ap.add_argument(
        "-p",
        "--live-server-port",
        help="The live development server's port",
        default=5500,
        type=int,
    )

    args = ap.parse_args()

    print("pykatana @ 2024 by Abolfazl Danayi (adanayidet@gmail.com)")

    if len(sys.argv) <= 1 and not args.build and not args.init and not args.server:
        print(
            """Welcome to the pykatana: A sword for Jinaj2!

Since you have not used any switches, I will run in normal mode!\n"""
        )
        print("\tChecking if folder is inited: ", flush=True, end="")
        if not os.path.exists("./src"):
            print("[No]\n\t\t", end="")
            _init()
        else:
            print("[Ok]")
        jinj = Jinjutsu("src", "./build")
        jinj.join(index_url="index.html", live_server_port=0, server=True, build=False)
        sys.exit(0)

    if "-i" in sys.argv:
        if os.path.exists("./src"):
            print(
                "src folder already exists. Can not re-initialize it. You should delete this folder yourself, if you want to reinit."
            )
            sys.exit(0)
        else:
            _init()
            print(
                """\n
                    1) You can now run the development server with -s switch.
                    2) You can use the ./archive folder to store your document files. This folder is git ignored. :D
            """
            )
            sys.exit(0)

    if not os.path.exists("./build"):
        os.makedirs("./build", exist_ok=True)

    if not os.path.exists("./src"):
        print(
            'pykatana error >>> "src" folder not found. You can use -i switch to initialize this project.'
        )
        sys.exit(0)

    for item in ("templates", "static", "meta"):
        if not os.path.exists(f"./src/{item}") or not os.path.isdir(f"./src/{item}"):
            print(
                f'pykatana warning >> "src/{item}" folder does not exist or it is not a folder...'
            )

    if not os.path.exists("./src/make.py"):
        print('pykatana error >>> "src/make.py" file not found...')
        sys.exit(1)

    jinj = Jinjutsu("src", "./build")
    jinj.join(index_url="index.html", **vars(args))
