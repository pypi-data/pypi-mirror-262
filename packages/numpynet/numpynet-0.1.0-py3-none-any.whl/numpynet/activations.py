from abc import ABC, abstractmethod

import numpy as np
from scipy.special import expit


class Activation(ABC):

    def __repr__(self):
        return self.__class__.__name__

    @abstractmethod
    def call(self, x):
        pass

    @abstractmethod
    def deriv(self, x):
        pass


class NoActivation(Activation):

    def call(self, x):
        return x.copy()

    def deriv(self, x):
        return np.ones_like(x)


class SigmoidActivation(Activation):

    def call(self, x):
        return expit(x)

    def deriv(self, x):
        y = self.call(x)
        return y * (1-y)


class ReLuActivation(Activation):

    def call(self, x):
        return np.maximum(x, 0)

    def deriv(self, x):
        return (x > 0).astype(np.float32)


class LeakyReLuActivation(Activation):

    def __init__(self, coef=0.1):
        self.coef = coef

    def call(self, x):
        return np.where(x > 0, x, self.coef*x)

    def deriv(self, x):
        return np.where(x > 0, 1, self.coef)


class TanhActivation(Activation):

    def call(self, x):
        return np.tanh(x)

    def deriv(self, x):
        return 1 - np.tanh(x) ** 2


class SinActivation(Activation):

    def call(self, x):
        return np.sin(x)

    def deriv(self, x):
        return np.cos(x)
