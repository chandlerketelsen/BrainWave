import torch
from tqdm import tqdm
from torch_geometric_temporal.nn.recurrent import EvolveGCNO

def save_checkpoint(model, optimizer, scheduler, epoch, train_losses, val_losses):
  checkpoint = {
          'epoch': epoch,
          'model_state_dict': model.state_dict(),
          'optimizer_state_dict': optimizer.state_dict(),
          'scheduler_state_dict': scheduler.state_dict(),
          'train_losses': train_losses,
          'val_losses': val_losses,
      }
  torch.save(checkpoint, f'/checkpoints/tfpp_checkpoint_{epoch}.pt')
  torch.save(model.state_dict(), f'/models/tfpp_model_{epoch}.pt')

def load_checkpoint(filepath, model, optimizer, scheduler):
    checkpoint = torch.load(filepath, map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
    start_epoch = checkpoint['epoch']
    train_losses = checkpoint['train_losses']
    val_losses = checkpoint['val_losses']
    return model, optimizer, scheduler, start_epoch, train_losses, val_losses

def train_loop(loader, model, criterion, optimizer, device, verbose=True):
    model.train()
    total_loss = 0.0
    num_batches = 0

    for t, snapshot in enumerate(tqdm(loader)):
        snapshot = snapshot.to(device)

        out = model(snapshot.x, snapshot.edge_index, snapshot.edge_attr)
        loss = criterion(out, snapshot.y.float())

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        num_batches += 1

        if verbose and (t + 1) % 100 == 0:
            print(f"Batch {t + 1}, Loss: {total_loss / num_batches:.6f}")

    return total_loss / max(1, num_batches)

def val_loop(loader, model, criterion, device, verbose=False):
    model.eval()
    total_loss = 0.0
    num_batches = 0

    with torch.no_grad():
        for t, snapshot in enumerate(loader):
            snapshot = snapshot.to(device)

            out = model(snapshot.x, snapshot.edge_index, snapshot.edge_attr)
            loss = criterion(out, snapshot.y.float())

            total_loss += loss.item()
            num_batches += 1

            if verbose and (t + 1) % 50 == 0:
                print(f"Val Batch {t + 1}")
                print(f"Preds:  {torch.sigmoid(out[:3])}")
                print(f"Target: {snapshot.y[:3]}")

    return total_loss / max(1, num_batches)