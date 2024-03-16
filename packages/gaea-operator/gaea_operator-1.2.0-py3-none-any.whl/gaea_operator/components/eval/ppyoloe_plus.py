#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/23
# @Author  : yanxiaodong
# @File    : eval_component.py
"""
import os
from argparse import ArgumentParser

from gaea_tracker import ExperimentTracker
from logit.base_logger import setup_logger
from windmillclient.client.windmill_client import WindmillClient

from gaea_operator.dataset import CocoDataset
from gaea_operator.trainer import Trainer


def parse_args():
    """
    Parse arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("--windmill_ak", type=str, default=os.environ.get("WINDMILL_AK"))
    parser.add_argument("--windmill_sk", type=str, default=os.environ.get("WINDMILL_SK"))
    parser.add_argument("--windmill_endpoint", type=str, default=os.environ.get("WINDMILL_ENDPOINT"))
    parser.add_argument("--windmill_tracking_uri", type=str, default=os.environ.get("WINDMILL_EXPERIMENT_KIND"))
    parser.add_argument("--windmill_experiment_name", type=str, default=os.environ.get("WINDMILL_EXPERIMENT_NAME"))
    parser.add_argument("--windmill_experiment_kind", type=str, default=os.environ.get("WINDMILL_TRACKING_URI"))
    parser.add_argument("--windmill_dataset_name", type=str, default=os.environ.get("WINDMILL_DATASET_NAME"))
    parser.add_argument("--intput_model_uri", type=str, default=os.environ.get("INPUT_MODEL_URI"))
    parser.add_argument("--output_dataset_uri", type=str, default=os.environ.get("OUTPUT_DATASET_URI"))
    parser.add_argument("--output_uri", type=str, default=os.environ.get("OUTPUT_URI"))
    args, _ = parser.parse_known_args()

    return args


def ppyoloe_plus_eval(args):
    """
    Eval component for ppyoloe_plus_m model.
    """
    windmill_client = WindmillClient(ak=args.windmill_ak,
                                     sk=args.windmill_sk,
                                     endpoint=args.windmill_endpoint)
    tracker_client = ExperimentTracker(windmill_client=windmill_client,
                                       tracking_uri=args.tracking_uri,
                                       experiment_name=args.experiment_name,
                                       experiment_kind=args.experiment_kind)
    setup_logger(config=dict(file_name=os.path.join(args.output_uri, "worker.log")))

    coco_dataset = CocoDataset(windmill_client=windmill_client, work_dir=tracker_client.work_dir)
    # 1. 合并分片数据集
    coco_dataset.concat_dataset(dataset_name=args.windmill_dataset_name,
                                output_dir=args.output_dataset_uri,
                                mode=CocoDataset.mode_keys[1])

    # 2. 评估
    Trainer(framework="PaddlePaddle").launch()


if __name__ == "__main__":
    args = parse_args()
    ppyoloe_plus_eval(args=args)