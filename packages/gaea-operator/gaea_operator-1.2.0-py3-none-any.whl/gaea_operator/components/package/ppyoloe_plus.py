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
from windmillmodelv1.client.model_api_model import parse_model_name, get_model_name
from windmillmodelv1.client.model_api_modelstore import parse_modelstore_name
from windmillartifactv1.client.artifact_api_artifact import get_name
from windmillclient.client.windmill_client import WindmillClient

from gaea_operator.config import PPYOLOEPLUSMConfig
from gaea_operator.model import format_name
from gaea_operator.utils import read_file, write_file


def parse_args():
    """
    Parse arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("--windmill_ak", type=str, default=os.environ.get("WINDMILL_AK"))
    parser.add_argument("--windmill_sk", type=str, default=os.environ.get("WINDMILL_SK"))
    parser.add_argument("--windmill_endpoint", type=str, default=os.environ.get("WINDMILL_ENDPOINT"))
    parser.add_argument("--windmill_project_name", type=str, default=os.environ.get("WINDMILL_PROJECT_NAME"))
    parser.add_argument("--windmill_public_modelstore", type=str, default=os.environ.get("WINDMILL_PUBLIC_MODELSTORE"))
    parser.add_argument("--windmill_tracking_uri", type=str, default=os.environ.get("WINDMILL_TRACKING_URI"))
    parser.add_argument("--windmill_experiment_name", type=str, default=os.environ.get("WINDMILL_EXPERIMENT_NAME"))
    parser.add_argument("--windmill_experiment_kind", type=str, default=os.environ.get("WINDMILL_EXPERIMENT_KIND"))
    parser.add_argument("--windmill_transform_model_name",
                        type=str,
                        default=os.environ.get("WINDMILL_TRANSFORM_MODEL_NAME"))
    parser.add_argument("--windmill_transform_model_display_name",
                        type=str,
                        default=os.environ.get("WINDMILL_TRANSFORM_MODEL_DISPLAY_NAME"))
    parser.add_argument("--windmill_ensemble_model_name",
                        type=str,
                        default=os.environ.get("WINDMILL_ENSEMBLE_MODEL_NAME"))
    parser.add_argument("--windmill_ensemble_model_display_name",
                        type=str,
                        default=os.environ.get("WINDMILL_ENSEMBLE_MODEL_DISPLAY_NAME"))
    parser.add_argument("--device_type", type=str, default=os.environ.get("DEVICE_TYPE", "nvidia"))

    parser.add_argument("--input_model_uri", type=str, default=os.environ.get("INPUT_MODEL_URI"))
    parser.add_argument("--output_model_uri", type=str, default=os.environ.get("OUTPUT_MODEL_URI"))
    parser.add_argument("--output_uri", type=str, default=os.environ.get("OUTPUT_URI"))

    args, _ = parser.parse_known_args()

    return args


def dump_template_model(windmill_client: WindmillClient, model_store_name: str, model_name: str, output_uri: str):
    """
    Dump template model.
    """
    ensemble_name = get_model_name(parse_modelstore_name(model_store_name)[0],
                                   parse_modelstore_name(model_store_name)[1],
                                   model_name)
    ensemble_artifact_name = get_name(object_name=ensemble_name,
                                      version="latest")
    windmill_client.dump(name=ensemble_artifact_name, output_uri=output_uri)


def ppyoloe_plus_package(args):
    """
    Package component for ppyoloe_plus model.
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

    response = read_file(input_dir=args.transform_model_uri)

    ensemble = "ppyoloeplus-ensemble"
    model = "ppyoloeplus-model"
    pre = "ppyoloeplus-preprocess"
    post = "ppyoloeplus-postprocess"

    ppyoloe_plus_model_to_res = {model: response}

    # 1. 下载ensemble template 模型
    dump_template_model(windmill_client=windmill_client,
                        model_store_name=args.windmill_public_modelstore,
                        model_name=ensemble,
                        output_uri=args.output_model_uri)

    # 2. 生成打包配置文件
    PPYOLOEPLUSMConfig(windmill_client=windmill_client). \
        write_triton_package_config(transform_model_uri=args.transform_model_uri,
                                    ensemble_model_uri=args.output_model_uri)

    workspace_id, model_store_name, ensemble_local_name = parse_model_name(name=args.windmill_model_name)
    # 3. 上传 Preprocess 模型
    pre_model_uri = os.path.join(args.output_model_uri, pre)
    local_name = format_name(args.windmill_transform_model_name, "pre")
    display_name = format_name(args.windmill_transform_model_display_name, "预处理")
    response = windmill_client.create_model(workspace_id=workspace_id,
                                            model_store_name=model_store_name,
                                            local_name=local_name,
                                            display_name=display_name,
                                            category="Image/Preprocess",
                                            model_formats=["Python"],
                                            artifact_uri=pre_model_uri)
    ppyoloe_plus_model_to_res.update({pre: response})

    # 4. 上传 PostProcess 模型
    post_model_uri = os.path.join(args.output_model_uri, post)
    local_name = format_name(args.windmill_transform_model_name, "post")
    display_name = format_name(args.windmill_transform_model_display_name, "后处理")
    response = windmill_client.create_model(workspace_id=workspace_id,
                                            model_store_name=model_store_name,
                                            local_name=local_name,
                                            display_name=display_name,
                                            category="Image/Postprocess",
                                            model_formats=["Python"],
                                            artifact_uri=post_model_uri)
    ppyoloe_plus_model_to_res.update({post: response})

    # 5. 修改 ensemble 配置文件
    ensemble_model_uri = os.path.join(args.output_model_uri, ensemble)
    PPYOLOEPLUSMConfig(windmill_client=windmill_client). \
        write_ensemble_config(ensemble_model_uri=ensemble_model_uri, model_config=ppyoloe_plus_model_to_res)

    # 6. 上传 ensemble 模型
    response = windmill_client.create_model(workspace_id=workspace_id,
                                            model_store_name=model_store_name,
                                            local_name=ensemble_local_name,
                                            display_name=args.windmill_ensemble_model_display_name,
                                            category="Image/Ensemble",
                                            model_formats=[
                                                PPYOLOEPLUSMConfig.device_type2model_format[args.device_type]],
                                            artifact_uri=ensemble_model_uri)

    # 4. 输出文件
    write_file(obj=response, output_dir=args.ensemble_model_uri)


if __name__ == "__main__":
    args = parse_args()
    ppyoloe_plus_package(args=args)
