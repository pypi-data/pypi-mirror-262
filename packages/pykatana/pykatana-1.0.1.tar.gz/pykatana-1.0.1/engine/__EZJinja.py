#
# بسم الله الرحمن الرحیم
# اللهم صل علی محمد و آل محمد
# ---------------------------
# Created on Fri Mar 01 2024
#
# Copyright (c) 2024 Abolfazl Danayi
# adanayidet@gmail.com
#


from distutils import extension
import jinja2 as J
import typing as T
import os
import shutil
from pathlib import Path
from .__dict import read_json
import sys


class EZJinja:
    def __init__(self, input_package_name: str, build_folder: str = "./build") -> None:
        """package_name: the folder name of package"""
        if not os.path.exists(input_package_name):
            raise Exception(
                f"Error: {os.path.abspath(input_package_name)} does not exist."
            )
        loader = J.FileSystemLoader('./src/templates')
        self.__env = J.Environment(
            loader=loader, autoescape=J.select_autoescape()
        )
        self.__package_name = input_package_name
        self.__build_folder = build_folder

        self.__inited = False

    @property
    def env(self) -> J.Environment:
        return self.__env

    def __from(self, *path) -> str:
        return os.path.join(self.__package_name, *path)

    def __to(self, *path) -> str:
        return os.path.join(self.__build_folder, *path)

    def build_path_of(self, *path) -> str:
        return os.path.join(os.path.abspath(self.__build_folder), *path)

    def clean(self):
        if os.path.exists(self.__build_folder):
            shutil.rmtree(self.__build_folder)
            os.makedirs(self.__build_folder)

    def init(self):
        if self.__inited:
            return
        self.clean()
        self.__inited = True

    def copy_static_folder(
        self,
        destination_folder: str = "static",
        exclude_extensions: T.Iterable = [],
        allow_extensions: T.Union[T.Iterable, None] = None,
    ):
        if self.__inited == False:
            raise Exception("Not inited yet. Call the init() function first.")
        if not os.path.exists(self.__from("static")):
            return

        def perform(f_from: str, f_to: str):
            objects = os.listdir(f_from)
            for item in objects:
                path_in = os.path.join(f_from, item)
                path_out = os.path.join(f_to, item)
                if os.path.isdir(path_in):
                    os.makedirs(path_out)
                    perform(path_in, path_out)
                else:
                    if "." in item:
                        extension = item.split(".")[-1]
                    else:
                        extension = ""
                    if (allow_extensions is None) or (extension in allow_extensions):
                        if not extension in exclude_extensions:
                            shutil.copyfile(path_in, path_out)

        if os.path.exists(self.__to(destination_folder)):
            shutil.rmtree(self.__to(destination_folder))
        os.makedirs(self.__to(destination_folder))
        perform(self.__from("static"), self.__to(destination_folder))

    def fetch_meta(self, meta_file_name: str) -> T.Union[dict, list]:
        if not meta_file_name.endswith(".json"):
            meta_file_name += ".json"
        jpath = self.__from(os.path.join("meta", meta_file_name))
        if not os.path.exists(jpath):
            raise Exception(f"Meta file @ {meta_file_name} does not exist.")
        return read_json(jpath)

    def export_template(
        self,
        template: str,
        output_path: T.Union[None, str] = None,
        post_process: callable = lambda x: x,
        *args,
        **kwargs,
    ):
        """Leave the output_path to None to use the template's path"""
        if self.__inited == False:
            raise Exception("Not inited yet. Call the init() function first.")
        if template.startswith("/"):
            template = template[1:]
        T = self.env.get_template(template)
        opath = template if output_path is None else output_path
        R = T.render(
            *args, **kwargs, enumerate=enumerate, len=len, meta=self.fetch_meta
        )
        parpath = Path(self.__to(opath)).parent.absolute()
        if not os.path.exists(parpath):
            os.makedirs(parpath)
        R = post_process(R)
        with open(self.__to(opath), "w", encoding="utf-8") as file:
            file.write(R)
