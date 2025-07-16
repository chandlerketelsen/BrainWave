import torch
from torch_geometric_temporal.nn.recurrent import GConvGRU
import torch.nn.functional as F

class TemporalGNN(torch.nn.Module):
    def __init__(self, node_features, hidden_features=64):
        super(TemporalGNN, self).__init__()
        self.recurrent = GConvGRU(in_channels=node_features, out_channels=hidden_features, K=2)
        self.linear = torch.nn.Linear(hidden_features, 1)

    def forward(self, x, edge_index, edge_weight):
        h = self.recurrent(x, edge_index, edge_weight)
        h = F.relu(h)
        h = self.linear(h).squeeze(-1)
        return h