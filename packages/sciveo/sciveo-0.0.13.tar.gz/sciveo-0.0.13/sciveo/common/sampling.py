#
# Pavlin Georgiev, Softel Labs
#
# This is a proprietary file and may not be copied,
# distributed, or modified without express permission
# from the owner. For licensing inquiries, please
# contact pavlin@softel.bg.
#
# 2023
#

from itertools import product
import numpy as np

from sciveo.common.configuration import Configuration


class BaseSampler:
  def __init__(self, configuration):
    self.configuration = configuration
    self.idx = 0

  def sample_min_max(self, min_value, max_value):
    return None

  def sample_list(self, list_values):
    return None

  # TODO: Need to refine dtypes, currently int/floats only supported.
  def minmax_dtype(self, min_value, max_value):
    if isinstance(min_value, int) and isinstance(max_value, int):
      return int
    elif isinstance(min_value, float) or isinstance(max_value, float):
      return float
    return float

  def sample_field(self, field):
    if isinstance(field, dict):
      if "values" in field:
        return self.sample_list(field["values"])
      elif "min" in field and "max" in field:
        return self.sample_min_max(field["min"], field["max"])
      elif "value" in field:
        return field["value"]
      elif "seq" in field:
        return field["seq"] * self.idx
      else:
        return None
    elif isinstance(field, list):
      return self.sample_list(field)
    elif isinstance(field, tuple) and len(field) >= 2:
      return self.sample_min_max(field[0], field[1])
    else:
      return field

  def __next__(self):
    sample = {}
    for k, v in self.configuration.items():
      sample[k] = self.sample_field(v)
    return Configuration(sample)

  def __call__(self):
    return next(self)

  def __iter__(self):
    return self


class RandomSampler(BaseSampler):
  def __init__(self, configuration):
    super().__init__(configuration)

  def sample_min_max(self, min_value, max_value):
    val = np.random.uniform(min_value, max_value)
    val = self.minmax_dtype(min_value, max_value)(val)
    return val

  def sample_list(self, list_values):
    return list_values[np.random.randint(0, len(list_values))]


class GridSampler(BaseSampler):
  def __init__(self, configuration):
    super().__init__(configuration)
    self.configuration_to_lists()
    self.sample_iterator = product(*self.configuration_lists.values())

  def configuration_field_to_list(self, field):
    if isinstance(field, dict):
      if "values" in field:
        return field["values"]
      elif "min" in field and "max" in field:
        default_num = 10
        if self.minmax_dtype(field["min"], field["max"]) == int:
          default_num = field["max"] - field["min"] + 1
        result = np.linspace(field["min"], field["max"], field.get("num", default_num))
        if self.minmax_dtype(field["min"], field["max"]) == int:
          result = result.astype(int)
        return result.tolist()
      elif "value" in field:
        return [field["value"]]
      else:
        return list(field.values())
    elif isinstance(field, list):
      return field
    elif isinstance(field, tuple) and len(field) >= 2:
      if len(field) >= 3:
        num = field[2]
      else:
        num = 10
        if self.minmax_dtype(field[0], field[1]) == int:
          num = field[1] - field[0] + 1
      result = np.linspace(field[0], field[1], num)
      if self.minmax_dtype(field[0], field[1]) == int:
        result = result.astype(int)
      return result.tolist()
    else:
      return [field]

  def configuration_to_lists(self):
    self.configuration_lists = {}
    for k, v in self.configuration.items():
      self.configuration_lists[k] = self.configuration_field_to_list(v)

  def __iter__(self):
    return self.sample_iterator

  def __next__(self):
    sample = next(self.sample_iterator)
    return Configuration(dict(zip(self.configuration_lists.keys(), sample)))
