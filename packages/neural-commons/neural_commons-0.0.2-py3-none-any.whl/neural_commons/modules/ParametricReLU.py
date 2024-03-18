import torch
from torch import nn


class ParametricReLU(nn.Module):
    def __init__(self, input_shape: tuple[int]):
        super(ParametricReLU, self).__init__()
        self.input_shape = input_shape
        self.slopes = nn.Parameter(torch.ones(input_shape).unsqueeze(0))

    def forward(self, x: torch.Tensor):
        positive = x >= 0
        return positive * x + (~positive) * x * self.slopes
