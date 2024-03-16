#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/26
# @Author  : yanxiaodong
# @File    : config.py
"""
import os
import shutil
from typing import Dict
from abc import ABCMeta, abstractmethod

from windmillclient.client.windmill_client import WindmillClient


class Config(metaclass=ABCMeta):
    """
    Config write for train, transform and package.
    """
    device_type_nvidia = "nvidia"
    device_type_r200 = "r200"
    device_type_k200 = "k200"
    device_type2model_format = {device_type_nvidia: "TensorRT",
                                device_type_r200: "PaddleLite",
                                device_type_k200: "PaddleLite"}

    def __init__(self, windmill_client: WindmillClient):
        self.windmill_client = windmill_client

    @abstractmethod
    def write_train_config(self,
                           dataset_uri: str,
                           pretrain_artifact_name: str,
                           model_uri: str):
        """
        Config write for train.
        """
        pass

    def write_eval_config(self, model_uri: str):
        """
        Config write for eval.
        """
        source_file = os.path.join(model_uri, self.eval_config_file_name)
        shutil.copyfile(source_file, self.default_eval_config_path)

    @abstractmethod
    def write_transform_config(self, model_uri: str, output_uri: str, device_type: str, **kwargs):
        """
        Config write for transform.
        """
        pass

    def write_triton_package_config(self,
                                    transform_model_uri: str,
                                    ensemble_model_uri: str,
                                    step_kind: str = "Postprocess"):
        """
        Config write for package.
        """
        pass

    def write_ensemble_config(self, ensemble_model_uri: str, model_config: Dict):
        """
        Config write for ensemble.
        """
        pass
