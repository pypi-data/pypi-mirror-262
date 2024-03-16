#
# بسم الله الرحمن الرحیم
# اللهم صل علی محمد و آل محمد
# ---------------------------
# Created on Fri Mar 01 2024
#
# Copyright (c) 2024 Abolfazl Danayi
# adanayidet@gmail.com
#


import typing as T
import json
import os


def fetch(src: dict, kw: str, default_value: any = None) -> T.Tuple[bool, any]:
    """Returns (found, value/default_value)
Note: dot hierarchy is allowed."""
    if '.' in kw:
        spl = kw.split('.')
        inner_src_kw = spl[0]
        rest_kw = '.'.join(spl[1:])
        if inner_src_kw in src:
            return fetch(src[inner_src_kw], rest_kw, default_value)
        else:
            return False, default_value
    else:
        if kw in src:
            return True, src[kw]
        else:
            return False, default_value


def read_json(file_path: str) -> T.Optional[dict]:
    """Reads the json file.
Note: returns None if the file_path does not exist"""
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'rb') as file:
        j = json.load(file)
        if type(j) == dict:
            if "___ In the name of" in j and j["___ In the name of"] == "Allah ___":
                j.pop("___ In the name of")
        else:
            if j[0] == "___ In the name of Allah ___":
                j = j[1:]
        return j


def write_json(D: T.Union[T.Dict, T.Iterable], file_path: str, **kwargs):
    if type(D) == dict:
        D = {"___ In the name of": "Allah ___", **D}
    else:
        D = ["___ In the name of Allah ___", *D]
    with open(file_path, 'w') as file:
        return json.dump(D, file, ensure_ascii=False, **kwargs)
