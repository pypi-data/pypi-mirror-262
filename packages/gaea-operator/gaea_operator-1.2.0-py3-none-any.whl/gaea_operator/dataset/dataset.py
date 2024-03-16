#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/21
# @Author  : yanxiaodong
# @File    : dataset_concat.py
"""
import json
import os
from abc import ABCMeta, abstractmethod
from typing import Any, List

import logit
from windmillclient.client.windmill_client import WindmillClient


class Dataset(metaclass=ABCMeta):
    """
    A dataset for data processing.
    """
    decompress_output_uri = "/root/dataset"
    mode_keys = ["", ""]

    def __init__(self, windmill_client: WindmillClient, work_dir: str):
        self.windmill_client = windmill_client
        self.work_dir = work_dir
        self.labels = []
        self.label_file_path = "labels.json"
        assert len(self.mode_keys) == 2, "Dataset mode keys length must equal 2"

    def concat_dataset(self, dataset_name: str, output_dir: str, mode: str):
        """
        Concat dataset from artifact.
        """
        logit.info(f"Concat dataset from {dataset_name}")
        response = self.windmill_client.get_artifact(name=dataset_name)
        filesystem = self.windmill_client.suggest_first_filesystem(workspace_id=response.workspaceID,
                                                                   guest_name=response.parentName)
        fs_prefix = self.windmill_client.build_base_uri(filesystem=filesystem)
        paths = [os.path.relpath(_path, fs_prefix).rstrip('/') for _path in response.metadata["paths"]]
        logit.info(f"Concat dataset from {paths}")

        raw_data = self._get_annotation(paths=paths, fs_prefix=fs_prefix, mode=mode)
        self._write_annotation(output_dir=output_dir, file_name=mode, raw_data=raw_data)

        if mode == self.mode_keys[0]:
            self._write_category(output_dir=output_dir)

    @abstractmethod
    def _get_annotation(self, paths: List, fs_prefix: str, mode: str):
        pass

    @abstractmethod
    def _write_annotation(self, output_dir: str, file_name: str, raw_data: Any):
        pass

    def _write_category(self, output_dir: str):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, self.label_file_path)
        with open(file_path, "w") as fp:
            json.dump(self.labels, fp)
