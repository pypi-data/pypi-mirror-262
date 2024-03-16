#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/27
# @Author  : yanxiaodong
# @File    : misc.py
"""
import json
import os
from typing import Dict


def find_upper_level_folder(path: str, level: int = 2):
    """
    Find the folder `levels` levels up from the given path.
    """
    upper_level = path
    for _ in range(level):
        upper_level = os.path.dirname(upper_level)
    return upper_level


def write_file(obj: Dict, output_dir: str, file_name: str = "response.json"):
    """
    Write the response list to a file.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, file_name), "w") as f:
        json.dump(obj, f, indent=4, ensure_ascii=False)


def read_file(input_dir: str, file_name: str = "response.json"):
    """
    Read the response list from a file.
    """
    with open(os.path.join(input_dir, file_name), "r") as f:
        data = json.load(f)

    return data


