#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/1
# @Author  : yanxiaodong
# @File    : Trainer.py
"""
import logit
from typing import List
import os
import time
import threading

from gaea_tracker import ExperimentTracker


from gaea_operator.metric import get_score_from_file


class Trainer(object):
    """
    Trainer class for different framework.
    """
    framework_paddlepaddle = "PaddlePaddle"
    framework_pytorch = "PyTorch"

    def __init__(self, framework: str, tracker_client: ExperimentTracker):
        self.framework = framework
        self.tracker_client = tracker_client

        self.training_exit_flag = False
        self._framework_check(framework=self.framework)

    def launch(self):
        """
        Launch the training process.
        """
        getattr(self, f"{self.framework.lower()}_launch")()

    def paddlepaddle_launch(self):
        """
        Launch the PaddleDetection training process.
        """
        from paddle.distributed.launch.main import launch
        launch()
        self.training_exit_flag = True

    @classmethod
    def _framework_check(cls, framework: str):
        frameworks = [cls.framework_paddlepaddle, cls.framework_pytorch]
        logit.info(f"framework: {framework}")

        assert framework in frameworks, f"framework must be one of {frameworks}, but get framework {framework}"

    def _track_thread(self, metric_names: List):
        while True:
            if self.training_exit_flag:
                break
            metric_filepath = os.path.join(self.tracker_client.job_work_dir, f"{self.tracker_client.run_id}.json")
            if os.path.exists(metric_filepath):
                for name in metric_names:
                    metric, epoch, step = get_score_from_file(metric_filepath, name)
                    if metric is not None:
                        logit.info(f"Track metric {name} with value: {metric} on step {step} or epoch {epoch}")
                        self.tracker_client.log_metrics(metrics={name: metric}, epoch=epoch, step=step)
            else:
                time.sleep(60)

    def track_model_score(self, metric_names: List):
        """
        Track the score of model.
        """
        thread = threading.Thread(target=self._track_thread, args=(metric_names, ))
        thread.start()
