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

import numpy as np


class BaseOptimizer:
  def __init__(self, keys, use_keys, learning_rate=0.01):
    # Negative learning rate, Y is loss and will optimize for minimum
    # Positive learning rate, Y is score and optimize for maximium
    self.learning_rate = learning_rate
    # Gradient based optimisation needs continuous parameters only.
    # So use keys list represents continuous params only. Remain keys list represents the non-continuous params list.
    self.keys = set(keys)
    self.use_keys = set(use_keys)
    self.remain_keys = self.keys - self.use_keys

  def x_to_list(self, x1, x2):
    list_x1 = []
    list_x2 = []
    for k in self.use_keys:
      list_x1.append(x1[k])
      list_x2.append(x2[k])
    return np.array(list_x1), np.array(list_x2)

  def list_to_x(self, x1, x2):
    dict_x = {}
    for k in self.remain_keys:
      dict_x[k] = x1[k]
    for i, k in enumerate(self.use_keys):
      dict_x[k] = x2[i]
    return dict_x

  def update(self, x, y, x_prev, y_prev):
    x1, x_prev1 = self.x_to_list(x, x_prev)

    delta_x = x1 - x_prev1
    delta_y = y - y_prev
    grads = delta_y / (delta_x + 1e-10)

    x_new = x1 * (1 + self.learning_rate * grads)

    return delta_y, self.list_to_x(x, x_new)


class AdamOptimizer(BaseOptimizer):
  def __init__(self, keys, use_keys, learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
    super().__init__(keys, use_keys, learning_rate)
    self.beta1 = beta1
    self.beta2 = beta2
    self.epsilon = epsilon
    self.t = 0
    self.m = None
    self.v = None

  def update(self, x, y, x_prev, y_prev):
    x1, x_prev1 = self.x_to_list(x, x_prev)

    if self.m is None:
      self.m = np.zeros_like(x1)
      self.v = np.zeros_like(x1)

    self.t += 1

    delta_x = x1 - x_prev1
    delta_y = y - y_prev
    grads = delta_y / (delta_x + 1e-10)

    self.m = self.beta1 * self.m + (1 - self.beta1) * grads
    self.v = self.beta2 * self.v + (1 - self.beta2) * (grads ** 2)

    m_hat = self.m / (1 - self.beta1 ** self.t)
    v_hat = self.v / (1 - self.beta2 ** self.t)

    x_new = x1 * (1 + self.learning_rate * m_hat / (np.sqrt(v_hat) + self.epsilon))

    return delta_y, self.list_to_x(x, x_new)
