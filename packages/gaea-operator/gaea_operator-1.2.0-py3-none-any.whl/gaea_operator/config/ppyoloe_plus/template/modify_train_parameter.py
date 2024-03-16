# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
#
"""
modify input train parameter yaml
Authors: wanggaofei(wanggaofei03@baidu.com)
Date:    2023-02-29
"""
import yaml
import argparse
import logit


KEY_EPOCH = 'epoch'
KEY_BASE_LR = 'base_lr'
KEY_WORKER_NUM = 'worker_num'
KEY_EVAL_HEIGHT = 'eval_height'
KEY_EVAL_WIDTH = 'eval_width'
KEY_BATCH_SIZE = 'batch_size'
KEY_PRETRAIN_WEIGHTS = 'pretrain_weights'
KEY_DEPTH_MULT = 'depth_mult'
KEY_WIDTH_MULT = 'width_mult'
KEY_SNAPSHOT_EPOCH = 'snapshot_epoch'
KEY_NUM_CLASSES = 'num_classes'
KEY_LEARNING_RATE = 'LearningRate'
KEY_SCHEDULERS = 'schedulers'
KEY_MAX_EPOCHS = 'max_epochs'
KEY_TRAIN_READER = 'TrainReader'
KEY_BATCH_TRANSFORMS = 'batch_transforms'
KEY_BATCH_RANDOM_RESIZE = 'BatchRandomResize'
KEY_TARGET_SIZE = 'target_size'

TARGET_SIZE_MAP = { '320,320': '[192, 224, 256, 288, 320, 352, 384, 416, 448]', 
                    '416,416': '[192,224,256,288,320,352,384,416,448,480,512,544]', 
                    '640,640': '[320, 352, 384, 416, 448, 480, 512, 544, 576, 608, 640, 672, 704, 736, 768]', 
                    '960,544': '[[224, 640], [256, 672], [288, 704], [320, 736], [352,768], [384,800], [416, 832], \
                        [448, 864], [480, 896], [512, 928], [544, 960], [576, 992], [608, 1024], \
                            [640, 1056], [672, 1088]]', 
                    '1280,736': '[[416, 960], [448, 992], [480, 1024], [512, 1056], [544, 1088], [576, 1120], \
                        [608, 1152], \
                        [640, 1184], [672, 1216], [704, 1248], [736, 1280], [768, 1312], [800, 1344], [832, 1376]]'
}

PRETRAIN_MODEL_NAMES = { \
 's': ['https://bj.bcebos.com/v1/paddledet/models/pretrained/ppyoloe_crn_s_obj365_pretrained.pdparams', 0.33, 0.50], 
 'm': ['https://bj.bcebos.com/v1/paddledet/models/pretrained/ppyoloe_crn_m_obj365_pretrained.pdparams', 0.67, 0.75], 
 'l': ['https://bj.bcebos.com/v1/paddledet/models/pretrained/ppyoloe_crn_l_obj365_pretrained.pdparams', 1.0, 1.0], 
 'x': ['https://bj.bcebos.com/v1/paddledet/models/pretrained/ppyoloe_crn_x_obj365_pretrained.pdparams', 1.33, 1.25]
}

def get_yaml(yaml_name):
    """
    读取指定YAML文件，并返回解析后的数据。如果读取失败，则返回None。
    
    Args:
        yaml_name (str): YAML文件的路径名。
    
    Returns:
        dict, optional: 返回一个字典类型，包含YAML文件中的内容；如果读取失败，则返回None。
    """
    with open(yaml_name) as f:
        yaml_data = yaml.load(f, Loader=yaml.Loader)
        return yaml_data
    return None

def save_yaml(yaml_data, yaml_name):
    """
    将字典数据保存为YAML格式的文件。
    
    Args:
        yaml_data (dict): 需要保存的字典数据。
        yaml_name (str): YAML文件名，包含路径。
    
    Returns:
        None; 无返回值，直接写入文件。
    """
    with open(yaml_name, 'w', encoding='utf-8') as f:
        yaml.dump(yaml_data, f, allow_unicode=True, sort_keys=False)

def set_value(yaml_data, key, val):
    """
    设置YAML数据中指定键的值，如果该键不存在则添加。如果键已经存在，将更新其值；否则，将添加一个新的键-值对。
    如果键不存在，将输出错误日志。
    
    Args:
        yaml_data (dict): YAML格式的数据，类型为字典，用于存储和修改键值对。
        key (str): 需要设置或添加的键名，类型为字符串。
        val (any): 需要设置或添加的键值，任意类型。
    
    Returns:
        None - 无返回值，直接修改传入的yamldata参数。
    
    Raises:
        None - 该函数没有引发任何异常。
    """
    if key in yaml_data:
        logit.info('old val. {} -> {}'.format(key, yaml_data[key]))
        yaml_data[key] = val
        logit.info('new val. {} -> {}'.format(key, yaml_data[key]))
    else:
        logit.error('do NOT find key: {}'.format(key))

def get_value(yaml_data, key):
    """
    根据指定的键值获取对应的值，如果找不到则返回None。
    
    Args:
        yaml_data (dict): YAML格式的数据字典。
        key (str): 需要查询的键值。
    
    Returns:
        Union[str, int, dict, list, None]: 如果找到该键值，则返回对应的值；否则返回None。
    """
    if key in yaml_data:
        return yaml_data[key]
    else:
        logit.info('do NOT find key: {}'.format(key))
        return None

def process_var(line, var_name, val):
    """
    处理变量
    """
    l = line.strip().split()
    if len(l) != 3:
        return line, False
    else:
        if str(l[0]) == var_name + ':' and str(l[1]) == '&' + var_name:
            return line.replace(l[-1], str(val)), True
        else:
            return line, False

def modify_var_value(yaml_name, var_name_vals):
    """
    处理变量
    """
    lines = []
    new_lines = []
    with open(yaml_name) as f:
        lines = f.readlines()
    for _, v in enumerate(lines):
        find = False
        for var_name, val in var_name_vals:
            if var_name in v:
                new_l, find = process_var(v, var_name, val)
                if find:
                    new_lines.append(new_l)
                    break
        
        if not find:
            new_lines.append(v)
    tmp_name = '/root/yaml_tmp.yaml' 
    with open(tmp_name, 'w') as f:
        for _, n in enumerate(new_lines):
            f.write(n)
    with open(tmp_name) as f:
        yaml_data = yaml.load(f, Loader=yaml.Loader)
    return yaml_data

def set_epoch(yaml_data, val):
    """
    设置给定的yaml_data中的epoch值为指定的val。如果原来的epoch值不等于val，则会记录日志。
    此外，如果学习率的scheduler中有max_epochs字段，并且大于当前的epoch值，则会将其修改为当前的epoch值。
    
    Args:
        yaml_data (dict): YAML格式的数据，包含epoch和learning rate相关的信息。
        val (int): 需要设置的epoch值，应该是一个整数。
    
    Returns:
        None; 无返回值，直接修改了yaml_data中的epoch值和learning rate的scheduler中的max_epochs值（如果存在）。
    """
    set_value(yaml_data, KEY_EPOCH, val)
    snapshot_epoch = get_value(yaml_data, KEY_SNAPSHOT_EPOCH)
    if snapshot_epoch is not None and int(snapshot_epoch) > val:
        set_value(yaml_data, KEY_SNAPSHOT_EPOCH, val)
    if KEY_LEARNING_RATE in yaml_data and KEY_SCHEDULERS in yaml_data[KEY_LEARNING_RATE]:
        for i in range(len(yaml_data[KEY_LEARNING_RATE][KEY_SCHEDULERS])):
            if KEY_MAX_EPOCHS in yaml_data[KEY_LEARNING_RATE][KEY_SCHEDULERS][i] and \
                int(yaml_data[KEY_LEARNING_RATE][KEY_SCHEDULERS][i][KEY_MAX_EPOCHS]) > val:
                yaml_data[KEY_LEARNING_RATE][KEY_SCHEDULERS][i][KEY_MAX_EPOCHS] = val
                logit.info('set-epoch modify max_epochs. {}'.format(val))

def set_base_lr(yaml_data, val):
    """
    设置基础学习率，如果不存在则创建
    
    Args:
        yaml_data (dict): YAML数据字典，包含学习率相关的键值对，如果不存在则会自动创建
        val (float): 要设置的基础学习率值
        
    Returns:
        None
        无返回值，直接修改传入的YAML数据字典中的基础学习率值
    """
    if KEY_LEARNING_RATE in yaml_data:
        set_value(yaml_data[KEY_LEARNING_RATE], KEY_BASE_LR, val)
    else:
        logit.error('do NOT find key: {}'.format(KEY_LEARNING_RATE))

def height_width_str2list(height_width_str):
    """
    字符串转列表
    """
    size_list = []
    s = height_width_str.strip()
    if s[0] == '[' and s[-1] == ']':
        s = s[1: -1].strip()
        if s[0] == '[' and s[-1] == ']':
            # height width independ
            s = s.replace('[', ' ').replace(']', ' ').split(',')
            for i in range(len(s) // 2):
                size_list.append([int(s[i * 2]), int(s[i * 2 + 1])])
        else:
            ws = s.split(',')
            for _, v in enumerate(ws):
                size_list.append(int(v))
    else:
        logit.error('invalid height-width-string. {}'.format(height_width_str))
    return size_list

def set_target_size(yaml_data, eval_width, eval_height):
    """
    设置目标大小，如果不支持该大小则报错。
    如果配置文件中存在train reader和batch transforms，并且包含batch random resize，则修改其target size为指定的大小。
    
    Args:
        yaml_data (dict): YAML格式的数据字典，包含train reader和batch transforms等信息。
        eval_width (int): 评估图像的宽度。
        eval_height (int): 评估图像的高度。
    
    Returns:
        None.
    
    Raises:
        ValueError: 如果不支持指定的目标大小。
    """
    eval_wh_str = str(eval_width) + ',' + str(eval_height)
    if eval_wh_str not in TARGET_SIZE_MAP:
        logit.error('do NOT support target size. width: {}, height: {}'.format(eval_width, eval_height))
    else:
        if KEY_TRAIN_READER in yaml_data and KEY_BATCH_TRANSFORMS in yaml_data[KEY_TRAIN_READER]:
            for _, v in enumerate(yaml_data[KEY_TRAIN_READER][KEY_BATCH_TRANSFORMS]):
                if KEY_BATCH_RANDOM_RESIZE in v and KEY_TARGET_SIZE in v[KEY_BATCH_RANDOM_RESIZE]:
                    v[KEY_BATCH_RANDOM_RESIZE][KEY_TARGET_SIZE] = height_width_str2list(TARGET_SIZE_MAP[eval_wh_str])
                    logit.info('set target size: {}'.format(eval_wh_str))

def set_model_type(yaml_data, val):
    """
    设置模型类型
    """
    model_type = val.strip().split('_')[-1]
    if model_type in PRETRAIN_MODEL_NAMES:
        name, depth_mult, width_mult = PRETRAIN_MODEL_NAMES[model_type]
        set_value(yaml_data, KEY_PRETRAIN_WEIGHTS, name)
        set_value(yaml_data, KEY_DEPTH_MULT, depth_mult)
        set_value(yaml_data, KEY_WIDTH_MULT, width_mult)
    else:
        logit.error('do NOT known model type value. {}'.format(val))

def set_batch_size(yaml_data, val):
    """
    设置批处理大小，如果不存在则返回False。
    该函数会修改传入的 yaml_data 中 KEY_TRAIN_READER 和 KEY_BATCH_SIZE 对应的值为给定的 val。
    如果不存在这两个键，则返回 False。
    
    Args:
        yaml_data (dict): YAML格式的字典，包含训练器相关配置信息，包括 KEY_TRAIN_READER 和 KEY_BATCH_SIZE。
        val (int): 要设置的新的批处理大小值。
    
    Returns:
        bool: 如果成功修改了批处理大小，返回 True；否则返回 False。
    
    Raises:
        None.
    """
    if KEY_TRAIN_READER in yaml_data and KEY_BATCH_SIZE in yaml_data[KEY_TRAIN_READER]:
        set_value(yaml_data[KEY_TRAIN_READER], KEY_BATCH_SIZE, val)
        logit.info('set {} -> {}'.format(KEY_BATCH_SIZE, val))
    else:
        logit.error('do NOT find key: {} or {}'.format(KEY_TRAIN_READER, KEY_BATCH_SIZE))

def parse_opt():
    """ parser opt
        Args:

        Returns:
            opt -- command line parameter
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_yaml', type=str, default="", help='output yaml file name')
    parser.add_argument('--epoch', type=str, default="", help='train epoch number')
    parser.add_argument('--base_lr', type=str, default="", help='base learning rate')
    parser.add_argument('--worker_num', type=str, default="", help='train-reader process number')
    parser.add_argument('--eval_height', type=str, default="", help='train model input height')
    parser.add_argument('--eval_width', type=str, default="", help='train model input width')
    parser.add_argument('--batch_size', type=str, default="", help='train batch size')
    parser.add_argument('--model_type', type=str, default="", help='model_type')
    parser.add_argument('--num_classes', type=str, default="", help='train dataset class number')
    option = parser.parse_args()
    return option

if __name__ == "__main__":
    opt = parse_opt()
    logit.info("args: {}".format(opt))

    # 0. eval_width/eval_height
    var_name_vals = [[KEY_EVAL_WIDTH, int(opt.eval_width)], [KEY_EVAL_HEIGHT, opt.eval_height]]
    
    if opt.model_type.startswith('change-'):
        input_yaml_name = '/root/parameter_c.yaml'
    else:
        input_yaml_name = '/root/parameter.yaml'

    logit.info('train parameter name: {}'.format(input_yaml_name))

    yaml_data = modify_var_value(input_yaml_name, var_name_vals)

    # 0. target_size
    set_target_size(yaml_data, opt.eval_width, opt.eval_height)

    # 1. epoch
    set_epoch(yaml_data, int(opt.epoch))

    # 2. base_lr
    set_base_lr(yaml_data, float(opt.base_lr))

    # 3. worker_num
    set_value(yaml_data, KEY_WORKER_NUM, int(opt.worker_num))

    # 3.1 num_classes
    set_value(yaml_data, KEY_NUM_CLASSES, int(opt.num_classes))

    # 4. model_type
    set_model_type(yaml_data, opt.model_type)

    # 5. batch_size
    set_batch_size(yaml_data, int(opt.batch_size))

    logit.info('begin to save yaml. {}'.format(opt.output_yaml))
    save_yaml(yaml_data, opt.output_yaml)
