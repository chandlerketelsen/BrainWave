import torch
from torch_geometric_temporal.nn.recurrent import GConvGRU
import torch.nn.functional as F

class TemporalForecastingGNN(torch.nn.Module):
    def __init__(self, node_features, hidden_features=256):
        super().__init__()
        self.recurrent1 = GConvGRU(in_channels=node_features, out_channels=hidden_features, K=5)
        self.recurrent2 = GConvGRU(in_channels=hidden_features, out_channels=hidden_features // 2, K=5)
        self.recurrent3 = GConvGRU(in_channels=hidden_features // 2, out_channels=hidden_features // 4, K=5)
        self.linear = torch.nn.Linear(hidden_features // 4, 1)

    def forward(self, x, edge_index, edge_weight):
        h = self.recurrent1(x, edge_index, edge_weight)
        h = F.relu(h)
        h = F.dropout(h, training=self.training)
        h = self.recurrent2(h, edge_index, edge_weight)
        h = F.relu(h)
        h = F.dropout(h, training=self.training)
        h = self.recurrent3(h, edge_index, edge_weight)
        h = F.relu(h)
        h = F.dropout(h, training=self.training)
        return self.linear(h).squeeze(-1)