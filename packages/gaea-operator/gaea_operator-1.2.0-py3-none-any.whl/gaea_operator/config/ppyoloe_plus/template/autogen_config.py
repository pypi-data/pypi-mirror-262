# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
#
"""
模型转换配置文件生成

Authors: zhouwenlong(zhouwenlong01@baidu.com)
Date:    2024/2/26 10:40
"""
import yaml
import logit
import argparse
import os


FRAMEWORK_LIST = ["onnx", "paddle"]
HARDWARE_LIST = ["k200", "r200", "nvidia", "bm1684x"]
MODEL_NAME_DICT = {"ppyoloe": ["image", "scale_factor"],
                  "change-ppyoloe": ["image", "tmp_image", "scale_factor"],
                  "vit-base": ["x"],
                  "resnet": ["x"],
                  "ocrnet": ["x"],
                  "maskformer": ["x"],
                  "change-ocrnet": ["x", "tmp_image"],
                  "co-detr": ["x"]
                  }  

def get_yaml(yaml_name):
    """
    读取指定的YAML文件，返回解析后的字典格式数据。如果YAML文件不存在，则抛出FileNotFoundError异常。
    
    Args:
        yaml_name (str): YAML文件名，包含路径信息。
    
    Returns:
        dict, None: 返回一个字典类型的数据，如果YAML文件内容为空或者无法解析，则返回None。
    
    Raises:
        FileNotFoundError: 当指定的YAML文件不存在时抛出此异常。
    """
    if not os.path.exists(yaml_name):
        raise FileNotFoundError(yaml_name)
    with open(yaml_name, 'r', encoding='utf-8') as f:
        file_data = f.read()

        yaml_data = yaml.load(file_data, Loader=yaml.FullLoader)
        return yaml_data

def _gen_input_shape(model_name, width, height, max_batch_size=1):
    """
    generate input shape 
    """
    batch = -1 if max_batch_size > 1 else 1
    input_shape = {}
    if model_name not in MODEL_NAME_DICT.keys():
        raise ValueError("model name not in model list")
        return
    if "ppyoloe" in model_name:
        input_shape = {"image": [batch, 3, height, width], "scale_factor": [batch, 2]}
        if "change" in model_name:
            input_shape["tmp_image"] = [batch, 3, height, width]
    elif "vit-base" in model_name or \
         "resnet" in model_name:
        input_shape["x"] = [batch, 3, height, width]
    elif "maskformer" in model_name or \
         "ocrnet" in model_name:
         logit.warn("maskformer and ocrnet not support batchsize > 1")
         batch = 1
         input_shape['x'] = [batch, 3, height, width]
         if "change" in model_name:
            input_shape['x'] = [batch, 6, height, width]
    else:
        raise ValueError("model name not in model list")
        return
    return input_shape

def _trans_shape(input_shape : dict) -> dict:
    """
    trans shape 
    """
    new_input_shape = {}
    for key, value in input_shape.items():
        if len(value) == 4:
            new_input_shape[key] = [value[0], value[2], value[3], value[1]]
        else:
            new_input_shape[key] = list(value)
    return new_input_shape

def create_common_config(source_framework: str, 
                  hardware: str, 
                  input_shape: dict,
                  cfg_path: str,
                  max_batch_size: int = 1, 
                  precision: str = "fp16",
                  max_boxes: int = None,
                  conf_thres: float = None,
                  iou_thres: float = None,
                  drop_nms: bool = False,
                  mean: dict = None,
                  std: dict = None,
                  rename_list: list = None,
                  transpose: bool = False,
                  norm: bool = False
                  ):
    """
    create config file for model tranform

    Args:
        source_framework (str): 输入模型框架格式，目前支持onnx和paddle 
        hardware (str): 目标硬件平台，目前支持k200、r200、nvidia、bm1684x
        input_shape (dict): 输入模型shape，类型为dict，例如{"image":[-1,3,640,640], "scale_factor":[-1,2]}
        cfg_path (str): 生成的转换配置文件保存路径
        max_batch_size (int): 最大batchsize，默认为1，当hardware为nvidia和bm1684x时生效
        max_boxes (int, optional): 输出的最大box num，当需要替换或添加nms操作时生效.默认为None，表示不进行nms的添加或替换
        conf_thres (float, optional): 替换或添加nms操作时的置信度门限. 默认为None，表示不进行nms的添加或替换
        iou_thres (float, optional): 替换或添加nms操作时的nms门限. 默认为None，表示不进行nms的添加或替换
        drop_nms (bool, optional): 替换或添加nms操作时，drop_nms=True时，只添加transpose和concat操作，方便检测模型接入自定义的nms. 默认为False
        mean (dict, optional): 为onnx模型添加预处理时的均值，类型为字典，例如{"image":[0.224,0.225,0.228]}. 默认为None，不添加预处理
        std (dict, optional): 为onnx模型添加预处理时的方差，类型为字典，例如{"image":[0.224,0.225,0.228]}. 默认为None，不添加预处理
        rename_list (list, optional): 为onnx模型修改输出名称. 类型为字典列表，
        例如[{concat_1.tmp_0:float32}, {concat_0.tmp_0:int64}], 顺序需要与模型输出顺序一致，数据类型也与模型输出一致。默认为None
        transpose (bool, optional): 为onnx模型添加预处理时，添加transpose操作. 默认为False，不添加
        norm (bool, optional): 为onnx模型添加预处理时，添加norm操作. 默认为False，不添加
        precision (str, optional): 精度. 默认为fp16， 可选为 fp32,fp16
    """
                  
    pipeline_cfg = []

    source_framework = source_framework.lower()
    hardware = hardware.lower()

    nms_params = None
    onnx_op_flag = False

    if max_boxes is not None and conf_thres is not None and iou_thres is not None:
        nms_params = {"max_boxes": max_boxes,
                       "conf_thres": conf_thres,
                       "iou_thres": iou_thres,
                       "drop_nms": drop_nms}
        logit.info("nms_params: {}".format(nms_params))
    
    # add OnnxToOnnx
    OnnxToOnnxParam = {}
    if mean is not None or std is not None or rename_list is not None or \
        transpose is not False or norm is not False or nms_params is not None:
        logit.info('use onnx2onnx mode.')
        onnx_op_flag = True
        OnnxToOnnxParam['type'] = 'OnnxToOnnx'
        OnnxToOnnxParam['input_shape'] = input_shape.copy()
        if 'scale_factor' in OnnxToOnnxParam['input_shape']:
            OnnxToOnnxParam['input_shape'].pop('scale_factor')
        if mean is not None and std is not None:
            OnnxToOnnxParam["mean"] = mean
            OnnxToOnnxParam["std"] = std
        if rename_list is not None:
            OnnxToOnnxParam["rename_list"] = rename_list
        OnnxToOnnxParam["transpose"] = transpose
        OnnxToOnnxParam["norm"] = norm
        if nms_params is not None:
            OnnxToOnnxParam["nms_params"] = nms_params

        logit.info("OnnxToOnnxParam = {}".format(OnnxToOnnxParam))

    # check args
    if source_framework not in FRAMEWORK_LIST:
        raise ValueError("{} is not supported".format(source_framework))
    if hardware not in HARDWARE_LIST:
        raise ValueError("{} is not supported".format(hardware))
    
    # convert_op_list = []
    # kunlun 
    if hardware in ["k200", "r200"]:
        OnnxToKunlunParam = {}
        if source_framework == "paddle":
            if onnx_op_flag and len(OnnxToOnnxParam) != 0 and nms_params is not None:
                # raise ValueError("nms_params is not supported for paddle to kunlun")
                logit.warning("ingore nms_params:[max_boxes, conf_thres ,iou_thres, drop_nms] for paddle to kunlun")
                OnnxToOnnxParam["nms_params"] = None

            if onnx_op_flag and len(OnnxToOnnxParam) != 0:
                PaddleToOnnxParam = {}
                PaddleToOnnxParam["type"] = "PaddleToOnnx"
                PaddleToOnnxParam["input_shape"] = input_shape
                pipeline_cfg.append(PaddleToOnnxParam)
                
                pipeline_cfg.append(OnnxToOnnxParam)

                OnnxToKunlunParam['type'] = 'OnnxToKunlun'
                OnnxToKunlunParam['device_type'] = hardware
                if len(OnnxToOnnxParam) > 0 and 'transpose' in OnnxToOnnxParam and OnnxToOnnxParam['transpose']:
                    OnnxToKunlunParam["input_shape"] = _trans_shape(input_shape)
                else:
                    OnnxToKunlunParam["input_shape"] = input_shape
                pipeline_cfg.append(OnnxToKunlunParam) 
            else:
                PaddleToKunlunParam = {}
                PaddleToKunlunParam["type"] = "PaddleToKunlun"
                PaddleToKunlunParam['device_type'] = hardware
                PaddleToKunlunParam["input_shape"] = input_shape
                # convert_op_list.append(PaddleToKunlunParam)
                pipeline_cfg.append(PaddleToKunlunParam)

        elif source_framework == "onnx":
            OnnxToKunlunParam['type'] = 'OnnxToKunlun'
            OnnxToKunlunParam["input_shape"] = input_shape
            pipeline_cfg.append(OnnxToKunlunParam) 

            if onnx_op_flag and len(OnnxToOnnxParam) != 0:
                pipeline_cfg.insert(0, OnnxToOnnxParam)
        else:
            raise NotImplementedError("{} is not supported".format(source_framework))
    # nvidia
    elif hardware == 'nvidia':
        if source_framework == "paddle":
            PaddleToOnnxParam = {}
            PaddleToOnnxParam["type"] = "PaddleToOnnx"
            PaddleToOnnxParam["model_name"] = "model"
            PaddleToOnnxParam["input_shape"] = input_shape
            pipeline_cfg.append(PaddleToOnnxParam)
        
        if onnx_op_flag:
            pipeline_cfg.append(OnnxToOnnxParam)
        
        OnnxToTensorrtParam = {}
        min_batch = 1
        opt_batch = max(max_batch_size // 2, 1)
        max_batch = max_batch_size

        OnnxToTensorrtParam["type"] = "OnnxToTensorRT"
        
        new_input_shape = {}
        new_input_shape_str = {}
        shape = {}
        if len(OnnxToOnnxParam) > 0 and 'transpose' in OnnxToOnnxParam and OnnxToOnnxParam['transpose']:
            new_input_shape = _trans_shape(input_shape)
        else:
            new_input_shape = input_shape

        for name, shape in new_input_shape.items():
            shape[0] = 1
            new_input_shape_str[name] = "x".join(str(x) for x in shape)

        cmd = ""
        for b, param_name in zip([min_batch, opt_batch, max_batch], ["--minShapes", "--optShapes", "--maxShapes"]):
            start_param = f"{param_name}="
            for name, shape in new_input_shape_str.items():
                shape = str(b) + shape[1:]
                start_param += name 
                start_param += ":"
                start_param += shape
                start_param += ","
            start_param = start_param[:-1]
            cmd += start_param + " "
        cmd += f" --workspace=2048 --{precision}"
        logit.info(f"OnnxToTensorrt cmd = {cmd}")

        OnnxToTensorrtParam["cmd"] = cmd
        
        pipeline_cfg.append(OnnxToTensorrtParam)
    #bitmain
    else:
        raise NotImplementedError("{} is not supported".format(hardware))
    
    cfg = {}
    cfg['pipeline'] = pipeline_cfg

    dir_name = os.path.dirname(cfg_path)
    if dir_name != "":
        os.makedirs(dir_name, exist_ok=True)

    with open(cfg_path, "w") as f:
        yaml.dump(cfg, f, indent=4)


def create_spec_config( source_framework: str, 
                        hardware: str,
                        model_name: str, 
                        height: int, 
                        width: int, 
                        max_batch_size: int, 
                        cfg_path: str, 

                        max_boxes: int = None,
                        conf_thres: float = None,
                        iou_thres: float = None,
                        precision: str = 'fp16'):
    """
    Create a config file for the specific model
    """                  
    model_name = model_name.lower()
    if model_name in ["ocrnet", "change-ocrnet", "maskformer", "co-detr"]:
        if max_batch_size > 1:
            logit.warning("max_batch_size is set to 1 for model {}".format(model_name))
            max_batch_size = 1
    input_shape = _gen_input_shape(model_name, height, width, max_batch_size)

    print(input_shape)
    
    try:
        create_common_config(source_framework, hardware, input_shape, cfg_path, 
                         max_batch_size=max_batch_size, 
                         conf_thres=conf_thres, 
                         iou_thres=iou_thres, 
                         precision=precision, 
                         transpose=False, 
                         norm=False, 
                         max_boxes=max_boxes)
    except Exception as e:
        logit.error(f"Failed to create config for {model_name} with error {e}")


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--hardware", type=str, required=True, default="bitmain")
    args.add_argument("--trans_param_path", type=str, required=True, default="")
    args.add_argument("--cfg_path", type=str, required=True, default="")
    args.add_argument("--max_batch", type=str, required=True, default="")
    args.add_argument("--max_boxes", type=str, required=False, default="")
    args.add_argument("--conf_thres", type=str, required=False, default="")
    args.add_argument("--iou_thres", type=str, required=False, default="")
    args.add_argument("--precision", type=str, required=False, default="fp16")

    args = args.parse_args()
    logit.info("args: {}".format(args))

    yaml_data = get_yaml(args.trans_param_path)

    width = yaml_data.get("width", None)
    height = yaml_data.get("height", None)
    source_framework = yaml_data.get("source_framework", None)
    model_name = yaml_data.get("model_name", None)

    if width is None or height is None or source_framework is None or model_name is None:
        logit.error("width, height, source_framework and model_name must be specified in the yaml file")
        raise ValueError("width, height, source_framework and model_name must be specified in the yaml file")
    
    try:
        hardware = args.hardware
        if hardware not in HARDWARE_LIST:
            raise ValueError("hardware must be one of {}".format(HARDWARE_LIST))
        max_batch = int(args.max_batch) if args.max_batch != "" else 1

        max_boxes = int(args.max_boxes) if args.max_boxes != "" else None
        conf_thres = float(args.conf_thres) if args.conf_thres != "" else None
        iou_thres = float(args.iou_thres) if args.iou_thres != "" else None
        precision = args.precision
        if precision not in ["fp16", "fp32"]:
            raise ValueError("precision must be fp16 or int8")
    except Exception as e:
        logit.error(f"Failed to parse max_batch, max_boxes, conf_thres and iou_thres with error {e}")
   
    cfg_path = args.cfg_path
    
    create_spec_config(source_framework, hardware, model_name, int(width), int(height), max_batch, cfg_path, 
                       max_boxes, conf_thres, iou_thres, precision)

    
