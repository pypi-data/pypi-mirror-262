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

import sciveo


class TestRunner(unittest.TestCase):
  def dummy_loop(self):
    with sciveo.open() as E:
      self.assertTrue(E.config.configuration.keys() == self.configuration.keys())

  def test_dummy_train(self):
    self.configuration = {
        "input_window": {
            "values": [10, 20, 30, 40, 50, 100, 200]
        },
        "steps": {
            "min": 1, "max": 100
        },
        "max_epochs": {
            "min": 1, "max": 3
        },
        "patience": {
            "min": 2, "max": 3
        },
        "idx": {
            "seq": 1
        }
    }

    for sampler in ["random", "grid"]:
      sciveo.start(
        project="SCIVEO Dummy Test",
        configuration=self.configuration,
        function=self.dummy_loop,
        remote=False,
        count=10,
        sampler=sampler
      )