import torch
import torch.nn as nn

class LinearPredictor(nn.Module):
    """
    Representação axiomática de uma camada linear para regressão vetorial.
    """
    def __init__(self, input_dim: int = 10, output_dim: int = 1):
        super().__init__()
        self.linear = nn.Linear(input_dim, output_dim)

    def forward(self, tensor_x: torch.Tensor) -> torch.Tensor:
        return self.linear(tensor_x)