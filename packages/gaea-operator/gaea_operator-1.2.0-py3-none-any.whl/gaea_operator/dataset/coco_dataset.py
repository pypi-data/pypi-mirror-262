#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/29
# @Author  : yanxiaodong
# @File    : coco_dataset.py
"""
import json
import os
from typing import Any, Dict, List

import logit
from windmillclient.client.windmill_client import WindmillClient

from .dataset import Dataset
from gaea_operator.utils import find_upper_level_folder, get_filepaths_in_archive


class CocoDataset(Dataset):
    """
    A Coco dataset for data processing.
    """
    mode_keys = ["train.json", "val.json"]

    def __init__(self, windmill_client: WindmillClient, work_dir: str):
        super().__init__(windmill_client=windmill_client, work_dir=work_dir)
        self.image_prefix_path = "images"

    def _get_annotation(self, paths: List, fs_prefix: str, mode: str):
        annotation_file_list = []
        for path in paths:
            path = os.path.join(self.work_dir, path)
            annotation_file_list = get_filepaths_in_archive(path, self.decompress_output_uri, mode)

        logit.info(f"[{mode.capitalize()}] annotation file list is: {annotation_file_list}")

        raw_data_list = []
        for file in annotation_file_list:
            json_data = json.load(open(file, "r"))
            images = json_data["images"]

            logit.info(f"Parse annotation file {file}, image num is {len(images)}")

            for img in images:
                img["file_name"] = self._file_name_cvt_abs(img["file_name"], file, fs_prefix)

            raw_data_list.append(json_data)

        if len(raw_data_list) > 1:
            raw_data_coco = self._coco_data_raw_concat(raw_data_list)
        elif len(raw_data_list) == 1:
            raw_data_coco = raw_data_list[0]
        else:
            raw_data_coco = None

        return raw_data_coco

    def _write_annotation(self, output_dir: str, file_name: str, raw_data: Any):
        if raw_data is None:
            return
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, "w") as fp:
            json.dump(raw_data, fp, ensure_ascii=False, indent=4)

    def _file_name_cvt_abs(self, image_file: str, json_file: str, fs_prefix: str):
        if image_file.startswith(fs_prefix):
            file = image_file.replace(fs_prefix, self.work_dir)
            return file
        if os.path.isabs(image_file):
            return image_file
        else:
            return os.path.join(find_upper_level_folder(json_file, 2), self.image_prefix_path, image_file)

    def _coco_data_raw_concat(self, raw_data: List[Dict]):
        cat_name2id = self._category_valid(raw_data)

        raw_data_coco = {"images": [], "annotations": [], "categories": raw_data[0]["categories"]}
        max_im_id = 1
        max_ann_id = 1

        for data in raw_data:
            old2new_im_id = {}
            old2new_cat_id = {}
            for img in data["images"]:
                max_im_id = self._get_max_id(img["id"], max_im_id)
                old2new_im_id[img["id"]] = max_im_id
                img["id"] = max_im_id
                raw_data_coco["images"].append(img)

            for cat in data["categories"]:
                if cat_name2id[cat["name"]] != cat["id"]:
                    old2new_cat_id[cat["id"]] = cat_name2id[cat["name"]]
                    cat["id"] = cat_name2id[cat["name"]]

            for ann in data["annotations"]:
                max_ann_id = self._get_max_id(ann["id"], max_ann_id)
                if ann["image_id"] in old2new_im_id:
                    ann["image_id"] = old2new_im_id[ann["image_id"]]
                if ann["category_id"] in old2new_cat_id:
                    ann["category_id"] = old2new_cat_id[ann["category_id"]]
                ann["id"] = max_ann_id
                raw_data_coco["annotations"].append(ann)

        return raw_data_coco

    def _get_max_id(self, im_id: int, max_im_id: int):
        if im_id > max_im_id:
            max_im_id = im_id

        return max_im_id

    def _category_valid(self, raw_data: List[Dict]):
        categories_list = [data["categories"] for data in raw_data]
        lengths = [len(categories) for categories in categories_list]

        if len(set(lengths)) == 1:
            logit.info(f"The number of categories is {lengths[0]}")
            cat_name2id = {cat["name"]: cat["id"] for cat in categories_list[0]}
            for idx in range(1, lengths[0]):
                for cat in categories_list[idx]:
                    if cat["name"] not in cat_name2id:
                        raise ValueError(f"The categories name is not equal, please check {categories_list}")
            self.categories = categories_list[0]
        else:
            raise ValueError(f"The number of categories is not equal, please check {categories_list}")