#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/7
# @Author  : yanxiaodong
# @File    : metric.py
"""
import os

from gaea_operator.utils import read_file


def get_score_from_file(filepath: str, metric_name: str):
    """
    Get metric name score from file.
    """
    metric_data = read_file(input_dir=os.path.dirname(filepath), file_name=os.path.basename(filepath))
    for metric in metric_data["metrics"]:
        if metric["name"] == metric_name:
            return metric["result"]