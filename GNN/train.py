import torch
from torch_geometric.loader import DataLoader
from model.GNN import TemporalGNN
from utils.train_utils import train_loop, val_loop, save_checkpoint
from utils.geometric_graphs import build_dataset

batch_size = 32
epochs = 30
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

distance_threshold = 75
sequence_length = 16

train_loader, val_loader = build_dataset("Data", dist_threshold=distance_threshold)

model = TemporalGNN(node_features=1).to(device)
for param in model.parameters():
    param.retain_grad()
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