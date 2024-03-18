from ..utils.shortcuts import get_initializer
from ..exceptions import InvalidShapeException
from .base import Layer


class DenseLayer(Layer):

    def __init__(self, neurons_count, initializer='glorot'):
        super().__init__()
        self.neurons_count = neurons_count
        self.initializer = get_initializer(initializer)
        self.weights = [None]
        self.__x = None

    @property
    def connections(self):
        return self.weights[0]

    @connections.setter
    def connections(self, value):
        self.weights[0] = value

    def validate_input_shape(self):
        if len(self.input_shape) != 1:
            raise InvalidShapeException(f'{self.__class__.__name__} input must be 1D, but is {self.input_shape}')

    def get_output_shape(self):
        return tuple((self.neurons_count,))

    def initialize(self):
        shape = (self.neurons_count, self.input_shape[0])
        initializer_kwargs = {
            'fan_in': self.input_shape[0],
            'fan_out': self.output_shape[0]
        }
        self.connections = self.initializer(shape, **initializer_kwargs)

    def propagate(self, x):
        self.__x = x
        return x @ self.connections.T

    def backpropagate(self, delta):
        next_delta = self.__get_next_delta(delta)
        self.__adjust_weights(delta)
        return next_delta

    def __adjust_weights(self, delta):
        weights_delta = self.nn.learning_rate * delta.reshape(-1, 1) @ self.__x.reshape(1, -1)
        self.connections -= weights_delta

    def __get_next_delta(self, delta):
        next_delta = delta @ self.connections
        return next_delta.flatten()
