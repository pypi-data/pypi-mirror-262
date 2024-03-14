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

from sciveo.common.sampling import RandomSampler, GridSampler


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
