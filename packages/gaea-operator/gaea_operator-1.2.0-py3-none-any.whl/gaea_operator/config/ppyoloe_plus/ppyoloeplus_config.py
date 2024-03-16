#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/1
# @Author  : yanxiaodong
# @File    : ppyoloeplus_config.py
"""
from gaea_operator.config.config import Config
import os
import json
import logging

from .template.modify_train_parameter import KEY_EVAL_WIDTH, \
    KEY_EVAL_HEIGHT, modify_var_value, set_target_size, \
    set_epoch, set_base_lr, set_value, set_model_type, set_batch_size, \
    save_yaml, KEY_WORKER_NUM, KEY_NUM_CLASSES
from .template.autogen_config import HARDWARE_LIST, create_spec_config

from gaea_operator.utils import DEFAULT_TRAIN_CONFIG_FILE_NAME


class PPYOLOEPLUSMConfig(Config):
    """
    Config write for train, transform and package.
    """

    def write_train_config(self,
                           dataset_uri: str,
                           model_uri: str,
                           eval_width: str,
                           eval_height: str,
                           model_type: str,
                           epoch: str,
                           base_lr: str,
                           worker_num: str,
                           batch_size: str,
                           pretrain_model_uri: str):
        """
        Config write for train of ppyoloe_plus_m model.
        """
        # 1. get model number
        tran_json_name = os.path.join(dataset_uri, 'labels.json')
        json_data = json.load(open(tran_json_name, "r"))
        num_classes = len(json_data)

        # 2. eval_width/eval_height
        var_name_vals = [[KEY_EVAL_WIDTH, int(eval_width)], [KEY_EVAL_HEIGHT, eval_height]]

        if model_type.startswith('change-'):
            input_yaml_name = 'template/parameter_c.yaml'
        else:
            input_yaml_name = 'template/parameter.yaml'

        logging.info('train parameter name: {}'.format(input_yaml_name))

        yaml_data = modify_var_value(input_yaml_name, var_name_vals)

        # 3. target_size
        set_target_size(yaml_data, eval_width, eval_height)

        # 4. epoch
        set_epoch(yaml_data, int(epoch))

        # 5. base_lr
        set_base_lr(yaml_data, float(base_lr))

        # 6. worker_num
        set_value(yaml_data, KEY_WORKER_NUM, int(worker_num))

        # 7 num_classes
        set_value(yaml_data, KEY_NUM_CLASSES, num_classes)

        # 8. model_type
        set_model_type(yaml_data, model_type)

        # 9. batch_size
        set_batch_size(yaml_data, int(batch_size))

        train_config_name = os.path.join(model_uri, DEFAULT_TRAIN_CONFIG_FILE_NAME)
        logging.info('begin to save yaml. {}'.format(train_config_name))

        save_yaml(yaml_data, train_config_name)

        logging.info('write train config finish.')

    def write_transform_config(self,
                               model_uri: str,
                               output_uri: str,
                               device_type: str,
                               iou_threshold: str,
                               conf_threshold: str,
                               max_box_num: str,
                               max_batch_size: str,
                               precision: str,
                               source_framework: str,
                               model_name: str,
                               width: str,
                               height: str):
        """
        Config write for transform of ppyoloe_plus_m model.
        """
        try:
            hardware = device_type
            if hardware not in HARDWARE_LIST:
                raise ValueError("hardware must be one of {}".format(HARDWARE_LIST))
            max_batch = int(max_batch_size) if max_batch_size != "" else 1

            max_boxes = int(max_box_num) if max_box_num != "" else None
            conf_thres = float(conf_threshold) if conf_threshold != "" else None
            iou_thres = float(iou_threshold) if iou_threshold != "" else None
            if precision not in ["fp16", "fp32"]:
                raise ValueError("precision must be fp16 or int8")
        except Exception as e:
            logging.error(f"Failed to parse max_batch, max_boxes, conf_thres and iou_thres with error {e}")

        cfg_path = os.path.join(output_uri, 'transform_config.yaml')

        create_spec_config(source_framework, hardware, model_name, int(width), int(height), max_batch, cfg_path,
                           max_boxes, conf_thres, iou_thres, precision)
