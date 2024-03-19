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

import os

from sciveo.common.tools.logger import *
from sciveo.common.sampling import RandomSampler, GridSampler, AutoSampler
from sciveo.content.project import RemoteProject, LocalProject


class ProjectRunner:
  current = None

  def __init__(self, project, function, remote=True, configuration={}, sampler="random", count=None):
    self.project_name = project
    self.function = function
    self.count = count

    if remote:
      self.project = RemoteProject(self.project_name)
    else:
      self.project = LocalProject(self.project_name)

    if sampler == "random":
      self.configuration_sampler = RandomSampler(configuration)
    elif sampler == "grid":
      self.configuration_sampler = GridSampler(configuration)
    elif sampler == "auto":
      self.configuration_sampler = AutoSampler(
        configuration, self.project,
        num_random_samples=10,
        next_sample_ratio=0.97,
        min_delta_score=0.01,
        optimizer="base",
        learning_rate=0.01
      )
    else:
      self.configuration_sampler = RandomSampler(configuration)

  def run(self):
    for i, configuration_sample in enumerate(self.configuration_sampler):
      if self.count is not None and i >= self.count:
        break

      self.project.config = configuration_sample
      self.project.config.set_name(f"[{self.project.list_content_size + i + 1}]")
      debug(type(self).__name__, "run", i, self.project.config)
      self.function()
