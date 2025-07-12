import torch
from torch_geometric.data import DataLoader
from model.GNN import TemporalGNN
from utils.train_utils import train_loop, val_loop, save_checkpoint
from utils.geometric_graphs import build_graph_dataset

batch_size = 32
epochs = 30
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

distance_threshold = 75
train_folder = ""
val_folder = ""
sequence_length = 16

train_data_list = build_graph_dataset(train_folder)
train_loader = DataLoader(train_data_list, batch_size=batch_size, shuffle=True)

val_data_list = build_graph_dataset(train_folder)
val_loader = DataLoader(val_data_list, batch_size=batch_size, shuffle=True)

model = TemporalGNN(node_features=1, periods=sequence_length, batch_size=batch_size).to(device)
learning_rate = 0.01
optimizer = torch.optim.AdamW(model.parameters(), lr=0.01, weight_decay=0.01, amsgrad=True)
criterion = torch.nn.BCEWithLogitsLoss()
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer=optimizer, T_max=epochs)

train_losses = []
val_losses = []

model.train()

for epoch in range(epochs):
    print(f"Epoch {epoch+1}")
    train_loss = train_loop(train_loader, model, criterion, optimizer, device)
    val_loss = val_loop(val_loader, model, criterion, device)

    scheduler.step()
    train_losses.append(train_loss)
    val_losses.append(val_loss)

    print(f"Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}")
    save_checkpoint(model, optimizer, scheduler, epoch, train_losses, val_losses)