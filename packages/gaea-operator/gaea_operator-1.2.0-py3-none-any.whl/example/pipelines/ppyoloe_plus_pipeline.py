#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/10
# @Author  : yanxiaodong
# @File    : ppyoloe_plus_m_pipeline.py
"""
from paddleflow.pipeline import Pipeline
from paddleflow.pipeline import CacheOptions
from paddleflow.pipeline import ContainerStep
from paddleflow.pipeline import Artifact

from gaea_operator.utils import DEFAULT_TRAIN_CONFIG_FILE_NAME, DEFAULT_PADDLEPADDLE_MODEL_FILE_NAME


@Pipeline(
    name="ppyoloe_plus_m",
    cache_options=CacheOptions(enable=True),
)
def pipeline(windmill_ak: str = "",
             windmill_sk: str = "",
             windmill_endpoint: str = "",
             experiment_kind: str = "",
             experiment_name: str = "",
             tracking_uri: str = "",
             project_name: str = "",
             train_dataset_name: str = "",
             val_dataset_name: str = "",
             train_model_name: str = "",
             train_model_display_name: str = "",
             eval_dataset_name: str = "",
             transform_model_name: str = "",
             transform_model_display_name: str = ""):
    """
    Pipeline for ppyoloe_plus_m training eval transform.
    """
    base_env = {"PF_JOB_FLAVOUR": "c4m16gpu1",
                "PF_JOB_QUEUE_NAME": "qa100",
                "WINDMILL_AK": windmill_ak,
                "WINDMILL_SK": windmill_sk,
                "WINDMILL_ENDPOINT": windmill_endpoint,
                "WINDMILL_EXPERIMENT_KIND": experiment_kind,
                "WINDMILL_EXPERIMENT_NAME": experiment_name,
                "WINDMILL_TRACKING_URI": tracking_uri,
                "WINDMILL_PROJECT_NAME": project_name}

    train_env = {"WINDMILL_TRAIN_DATASET_NAME": train_dataset_name,
                 "WINDMILL_VAL_DATASET_NAME": val_dataset_name,
                 "WINDMILL_MODEL_NAME": train_model_name,
                 "WINDMILL_MODEL_DISPLAY_NAME": train_model_display_name,
                 "EPOCH": "1",
                 "BASE_LR": "0.001",
                 "WORKER_NUM": "4",
                 "EVAL_HEIGHT": "640",
                 "EVAL_WIDTH": "640",
                 "BATCH_SIZE": "4",
                 "MODEL_TYPE": "ppyoloe_m"}
    train_env.update(base_env)
    train = ContainerStep(name="train",
                          docker_env="iregistry.baidu-int.com/windmill-public/train:v1.2.0",
                          env=train_env,
                          outputs={"output_model_uri": Artifact(), "output_uri": Artifact()},
                          command=f'package_path=$(python3 -c "import site; print(site.getsitepackages()[0])") && '
                                  f'python3 -m gaea_operator.components.train.ppyoloe_plus '
                                  f'--output_model_uri={{{{output_model_uri}}}} '
                                  f'--output_uri={{{{output_uri}}}} '
                                  f'--log_dir={{{{output_uri}}}} '
                                  f'$package_path/paddledet/tools/train.py '
                                  f'-c {{{{output_model_uri}}}}/{DEFAULT_TRAIN_CONFIG_FILE_NAME} '
                                  f'-o save_dir={{{{output_model_uri}}}}')

    eval_env = {"WINDMILL_DATASET_NAME": eval_dataset_name}
    eval_env.update(base_env)
    eval = ContainerStep(name="eval",
                         docker_env="iregistry.baidu-int.com/windmill-public/train:v1.2.0",
                         env=eval_env,
                         inputs={"input_model_uri": train.outputs["output_model_uri"]},
                         outputs={"output_uri": Artifact(), "output_dataset_uri": Artifact()},
                         command=f'package_path=$(python3 -c "import site; print(site.getsitepackages()[0])") && '
                                 f'python3 -m gaea_operator.components.eval.ppyoloe_plus '
                                 f'--input_model_uri={{{{input_model_uri}}}} '
                                 f'--output_uri={{{{output_uri}}}} '
                                 f'--output_dataset_uri={{{{output_dataset_uri}}}} '
                                 f'--log_dir={{{{output_uri}}}} '
                                 f'$package_path/paddledet/tools/eval.py '
                                 f'-c {{{{input_model_uri}}}}/{DEFAULT_TRAIN_CONFIG_FILE_NAME} '
                                 f'-o weights={{{{input_model_uri}}}}/{DEFAULT_PADDLEPADDLE_MODEL_FILE_NAME}')

    transform_env = {"WINDMILL_MODEL_NAME": transform_model_name,
                     "WINDMILL_MODEL_DISPLAY_NAME": transform_model_display_name,
                     "DEVICE_TYPE": "nvidia",
                     "IOU_THRESHOLD": "0.45",
                     "CONF_THRESHOLD": "0.1",
                     "MAX_BOX_NUM": "30",
                     "MAX_BATCH_SIZE": "1",
                     "PRECISION": "fp16",
                     "MODEL_TYPE": "ppyoloe_m",
                     "EVAL_HEIGHT": "640",
                     "EVAL_WIDTH": "640"}
    transform_env.update(base_env)
    transform = ContainerStep(name="transform",
                              docker_env="iregistry.baidu-int.com/acg_aiqp_algo/model_convert:4.2.0",
                              env=transform_env,
                              inputs={"input_model_uri": train.outputs["output_model_uri"]},
                              outputs={"output_model_uri": Artifact(), "output_uri": Artifact()},
                              command=f'python3 -m gaea_operator.components.transform.transform '
                                      f'--input_model_uri={{{{input_model_uri}}}} '
                                      f'--output_uri={{{{output_uri}}}} '
                                      f'--output_model_uri={{{{output_model_uri}}}}')

    return transform.outputs["output_model_uri"]


if __name__ == "__main__":
    pipeline_client = pipeline(windmill_ak="1cb1860b8bc848298050edffa2ef9e16",
                               windmill_sk="51a7a74c9ef14063a6892d08dd19ffbf",
                               windmill_endpoint="http://10.27.240.45:8340",
                               experiment_kind="Aim",
                               experiment_name="ppyoloe_plus_m",
                               tracking_uri="aim://10.27.240.45:8329",
                               project_name="workspaces/default/projects/proj-UKm2uVsG",
                               train_dataset_name=
                               "workspaces/default/projects/proj-UKm2uVsG/datasets/ds-aanoGFeu/versions/1",
                               val_dataset_name=
                               "workspaces/default/projects/proj-UKm2uVsG/datasets/ds-aanoGFeu/versions/1",
                               eval_dataset_name=
                               "workspaces/default/projects/proj-UKm2uVsG/datasets/ds-aanoGFeu/versions/1",
                               train_model_name="workspaces/default/modelstores/ms-p6z2aKJp/models/ppyoloe-plus",
                               train_model_display_name="ppyoloe_plus",
                               transform_model_name=
                               "workspaces/default/modelstores/ms-p6z2aKJp/models/ppyoloe-plus-t4",
                               transform_model_display_name="ppyoloe-plus-t4")
    pipeline_client.compile(save_path="ppyoloe_plus_m_pipeline.yaml")
    _, run_id = pipeline_client.run(fs_name="spi")
    print(f"run_id: {run_id}")
