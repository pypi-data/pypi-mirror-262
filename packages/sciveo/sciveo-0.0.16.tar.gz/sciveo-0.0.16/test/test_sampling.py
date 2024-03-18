#
# Pavlin Georgiev, Softel Labs
#
# This is a proprietary file and may not be copied,
# distributed, or modified without express permission
# from the owner. For licensing inquiries, please
# contact pavlin@softel.bg.
#
# 2024
#

import unittest
import numpy as np

from sciveo.common.sampling import RandomSampler, GridSampler, AutoSampler
from sciveo.content.project import RemoteProject, LocalProject
from sciveo.common.optimizers import AdamOptimizer, BaseOptimizer


class TestSampling(unittest.TestCase):
  def check_sampling_names(self, class_name):
    config = {
        "booster": {
            "values": ["gbtree", "gblinear"]
        },
        "booster2": ["gbtree", "gblinear"],
        "learning_rate": {
          "min": 0.001,
          "max": 1.0,
          "num": 100
        },
        "gamma": {
          "min": 0.001,
          "max": 1.0,
          "num": 1000
        },
        "max_depth": {
            "values": [3, 5, 7]
        },
        "min_child_weight": {
          "min": 1,
          "max": 150,
          "num": 150
        },
        "early_stopping_rounds": {
          "values" : [10, 20, 30, 40]
        },
    }

    sampler = class_name(config)
    s = next(sampler)
    for k in s.configuration.keys():
      self.assertTrue(k in config.keys())

  def check_config_fields(self, class_name):
    config = {
        "C1": {
          "values": ["gbtree", "gblinear"]
        },
        "C2": ["gbtree", "gblinear"],
        "C3": {
          "min": 0.001, "max": 1.0
        },
        "C4": {
          "values" : [10, 20, 30, 40]
        },
        "C5": 1.23,
        "C6": {
          "min": 1, "max": 10
        },
        "C7": (1.0, 2.2),
        "C8": (1, 10),

        "C9": {
          "min": 11, "max": 20
        },
        "C10": (11, 20),
        "C11": (0.01, 1.0, 100),
        "C12": {
          "min": 0.01, "max": 1.0, "num": 100
        }
    }

    sampler = class_name(config)
    c = sampler()

    self.assertTrue(c("C5") == config["C5"])

    # Test in values list
    for k in ["C1", "C4"]:
      self.assertTrue(c(k) in config[k]["values"])
    # Test in list
    for k in ["C2"]:
      self.assertTrue(c(k) in config[k])
    # Test tuples numbers in the range
    for k in ["C7", "C8", "C10", "C11"]:
      self.assertTrue(config[k][0] <= c(k) and c(k) <= config[k][1])
    # Test min/max numbers in the range
    for k in ["C3", "C6", "C9", "C12"]:
      self.assertTrue(config[k]["min"] <= c(k) and c(k) <= config[k]["max"])
    # Test for int
    for k in ["C4", "C6", "C8", "C9", "C10"]:
      self.assertTrue(isinstance(c(k), int))
    # Test for float
    for k in ["C3", "C5", "C7", "C11", "C12"]:
      self.assertTrue(isinstance(c(k), float))
    # Test for string
    for k in ["C1", "C2"]:
      self.assertTrue(isinstance(c(k), str))

  def test_samplers(self):
    for class_name in [RandomSampler, GridSampler]:
      self.check_sampling_names(class_name)
      self.check_config_fields(class_name)


class TestBaseOptimizer(unittest.TestCase):
  def optimize(self, params, prev_params, fn_score, optimizer, n=10000, max_delta_score=1e-10):
    score = fn_score(params)
    prev_score = fn_score(prev_params)

    for i in range(n):
      # print(params, prev_params)
      delta_score, new_params = optimizer.update(
        params, score,
        prev_params, prev_score
      )
      prev_params, prev_score = params, score
      params, score = new_params, fn_score(new_params)
      if np.linalg.norm(delta_score) < max_delta_score:
        break
    # print(i, params, score)
    return params, score

  def test_sin_max(self):
    fn_score = lambda params: np.sin(params['x1']) + np.sin(2 * params['x1'])

    max_x = 0.93593
    max_y = fn_score({"x1": max_x})

    keys = ["x1"]
    use_keys = ["x1"]

    # High precision, high number of steps
    for optimizer in [BaseOptimizer(keys, use_keys, learning_rate=0.03), AdamOptimizer(keys, use_keys, learning_rate=0.01)]:
      for x1 in [0.1, 2.0]:
        params, score = self.optimize({"x1": x1}, {"x1": x1 * 0.99}, fn_score, optimizer, max_delta_score=1e-5)
        # print(type(optimizer).__name__, params['x1'], score)
        # print(type(optimizer).__name__, np.abs(params['x1'] - max_x), np.abs(score - max_y))
        self.assertTrue(np.abs(params['x1'] - max_x) < 0.01)
        self.assertTrue(np.abs(score - max_y) < 0.01)

    # Normal precision (1% - 5%) low number of steps
    for optimizer in [BaseOptimizer(keys, use_keys, learning_rate=0.05), AdamOptimizer(keys, use_keys, learning_rate=0.05)]:
      for x1 in [0.1, 2.0]:
        params, score = self.optimize({"x1": x1}, {"x1": x1 * 0.99}, fn_score, optimizer, n=100, max_delta_score=1e-5)
        # print(type(optimizer).__name__, "X", params['x1'], "Y", score)
        # print(type(optimizer).__name__, np.abs(params['x1'] - max_x), np.abs(score - max_y))
        self.assertTrue(np.abs(params['x1'] - max_x) < 0.05)
        self.assertTrue(np.abs(score - max_y) < 0.05)

    # There is a small local maximum and testing the escape capability to find the bigger maximum.
    # for x1 in [4.2]:
    #   params, score = self.optimize({"x1": x1}, {"x1": x1 * 0.99}, fn_score, AdamOptimizer(keys, use_keys, learning_rate=0.001, beta1=0.8, beta2=0.9))
    #   self.assertTrue(np.abs(params['x1'] - max_x) < 1e-4)
    #   self.assertTrue(np.abs(score - max_y) < 1e-4)

  def test_non_continuous(self):
    fn_score = lambda params: np.sin(params['x1']) + np.sin(2 * params['x1'])

    max_x = 0.93593

    config = {
      "x1": max_x,
      "batch_size": 8
    }

    max_y = fn_score(config)

    use_keys = ["x1"]

    # High precision, high number of steps
    for optimizer in [BaseOptimizer(config.keys(), use_keys, learning_rate=0.001), AdamOptimizer(config.keys(), use_keys, learning_rate=0.001)]:
      for x1 in [0.1, 2.0]:
        current_sample = config.copy()
        current_sample["x1"] = x1
        prev_sample = config.copy()
        prev_sample["x1"] = x1 * 0.99

        params, score = self.optimize(current_sample, prev_sample, fn_score, optimizer)
        self.assertTrue(np.abs(params['x1'] - max_x) < 1e-4)
        self.assertTrue(np.abs(score - max_y) < 1e-4)


class TestAutoSampling(unittest.TestCase):
  def test_sampling(self):
    config = {
      "lr": (0.001, 0.1, 10),
      "gamma": (0.01, 1.0),
      "batch_size": [4, 8, 16, 32]
    }

    project = LocalProject("test")
    sampler = AutoSampler(config, project, num_random_samples=3)

    for i, configuration_sample in enumerate(sampler):
      print("TestAutoSampling", i, configuration_sample)
      project.config = configuration_sample
      E = project.open()
      E.score(i * 0.01)
      project.close()
