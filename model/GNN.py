import torch
from torch_geometric_temporal.nn.recurrent import A3TGCN2
import torch.nn.functional as F

class TemporalGNN(torch.nn.Module):
    def __init__(self, node_features, periods=16, batch_size=32):
        super().__init__()
        self.a3tgcn1 = A3TGCN2(in_channels=node_features, out_channels=64, periods=periods, batch_size=batch_size)
        self.a3tgcn2 = A3TGCN2(in_channels=64, out_channels=64, periods=periods, batch_size=batch_size)
        self.linear = torch.nn.Linear(64, 1)

    def forward(self, x, edge_index):
        h = self.a3tgcn1(x, edge_index)
        h = F.relu(h)
        h = self.a3tgcn2(h, edge_index)
        h = F.relu(h)
        h = self.linear(h).squeeze(-1)
        return h