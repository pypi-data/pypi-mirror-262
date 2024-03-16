#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/23
# @Author  : yanxiaodong
# @File    : transform_component.py
"""
import os
from argparse import ArgumentParser

from gaea_tracker import ExperimentTracker
from logit.base_logger import setup_logger
from windmillmodelv1.client.model_api_model import parse_model_name
from windmillclient.client.windmill_client import WindmillClient

from gaea_operator.config import Config
from gaea_operator.utils import write_file


def parse_args():
    """
    Parse arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("--windmill_ak", type=str, default=os.environ.get("WINDMILL_AK"))
    parser.add_argument("--windmill_sk", type=str, default=os.environ.get("WINDMILL_SK"))
    parser.add_argument("--windmill_endpoint", type=str, default=os.environ.get("WINDMILL_ENDPOINT"))
    parser.add_argument("--windmill_project_name", type=str, default=os.environ.get("WINDMILL_PROJECT_NAME"))
    parser.add_argument("--windmill_tracking_uri", type=str, default=os.environ.get("WINDMILL_TRACKING_URI"))
    parser.add_argument("--windmill_experiment_name", type=str, default=os.environ.get("WINDMILL_EXPERIMENT_NAME"))
    parser.add_argument("--windmill_experiment_kind", type=str, default=os.environ.get("WINDMILL_EXPERIMENT_KIND"))
    parser.add_argument("--windmill_transform_model_name",
                        type=str,
                        default=os.environ.get("WINDMILL_TRANSFORM_MODEL_NAME"))
    parser.add_argument("--windmill_transform_model_display_name",
                        type=str,
                        default=os.environ.get("WINDMILL_TRANSFORM_MODEL_DISPLAY_NAME"))
    parser.add_argument("--device_type", type=str, default=os.environ.get("DEVICE_TYPE", "nvidia"))
    parser.add_argument("--iou_threshold", type=str, default=os.environ.get("IOU_THRESHOLD", "0.45"))
    parser.add_argument("--conf_threshold", type=str, default=os.environ.get("CONF_THRESHOLD", "0.1"))
    parser.add_argument("--max_box_num", type=str, default=os.environ.get("EVAL_HEIGHT", "30"))
    parser.add_argument("--max_batch_size", type=str, default=os.environ.get("EVAL_WIDTH", "1"))
    parser.add_argument("--precision", type=str, default=os.environ.get("BATCH_SIZE", "fp16"))
    parser.add_argument("--model_type", type=str, default=os.environ.get("MODEL_TYPE", "ppyoloe_m"))
    parser.add_argument("--eval_height", type=str, default=os.environ.get("EVAL_HEIGHT", "640"))
    parser.add_argument("--eval_width", type=str, default=os.environ.get("EVAL_WIDTH", "640"))

    parser.add_argument("--input_model_uri", type=str, default=os.environ.get("INPUT_MODEL_URI"))
    parser.add_argument("--output_model_uri", type=str, default=os.environ.get("OUTPUT_MODEL_URI"))
    parser.add_argument("--output_uri", type=str, default=os.environ.get("OUTPUT_URI"))

    args, _ = parser.parse_known_args()

    return args


def transform(args):
    """
    Transform component for model.
    """
    windmill_client = WindmillClient(ak=args.windmill_ak,
                                     sk=args.windmill_sk,
                                     endpoint=args.windmill_endpoint)
    tracker_client = ExperimentTracker(windmill_client=windmill_client,
                                       tracking_uri=args.windmill_tracking_uri,
                                       experiment_name=args.windmill_experiment_name,
                                       experiment_kind=args.windmill_experiment_kind,
                                       project_name=args.windmill_project_name)
    setup_logger(config=dict(file_name=os.path.join(args.output_uri, "worker.log")))

    # 1. 生成转换配置文件，固定名称 transform_config.yaml 保存在 output_uri
    Config(windmill_client=windmill_client).write_transform_config(model_uri=args.input_model_uri,
                                                                   output_uri=args.ouput_model_uri,
                                                                   device_type=args.device_type,
                                                                   iou_threshold=args.iou_threshold,
                                                                   conf_threshold=args.conf_threshold,
                                                                   max_box_num=args.max_box_num,
                                                                   max_batch_size=args.max_batch_size,
                                                                   precision=args.precision,
                                                                   model_type=args.model_type,
                                                                   width=args.eval_width,
                                                                   height=args.eval_height)

    # 2. 转换

    # 3. 上传转换后的模型
    workspace_id, model_store_name, local_name = parse_model_name(name=args.model_name)
    response = windmill_client.create_model(artifact_uri=args.transform_model_uri,
                                            workspace_id=workspace_id,
                                            model_store_name=model_store_name,
                                            local_name=local_name,
                                            display_name=args.model_display_name,
                                            category="Image/ObjectDetection",
                                            model_formats=[
                                                Config.device_type2model_format[args.device_type]])

    # 4. 输出文件
    write_file(obj=response, output_dir=args.output_model_uri)


if __name__ == "__main__":
    args = parse_args()
    transform(args=args)
