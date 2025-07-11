import torch
from tqdm import tqdm

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

def train_loop(train_loader, model, criterion, optimizer, device, verbose=True):
    model.train()
    total_loss = 0.0
    num_batches = len(train_loader)

    for batch_idx, batch in enumerate(tqdm(train_loader)):
        batch = batch.to(device)

        x = batch.x
        edge_index = batch.edge_index
        y = batch.y.float()

        optimizer.zero_grad()
        out = model(x, edge_index)
        loss = criterion(out, y)

        loss.backward()
        optimizer.step()

        total_loss += loss.item()

        if (batch_idx + 1) % 100 == 0 and verbose:
            print(f"Batch {batch_idx+1}, Loss: {total_loss / (batch_idx + 1):.6f}")

    return total_loss / num_batches

def val_loop(val_loader, model, criterion, device, verbose=False):
    model.eval()
    total_loss = 0.0
    num_batches = len(val_loader)

    with torch.no_grad():
        for batch_idx, batch in enumerate(val_loader):
            batch = batch.to(device)

            x = batch.x
            edge_index = batch.edge_index
            y = batch.y.float()

            out = model(x, edge_index)
            loss = criterion(out, y)
            total_loss += loss.item()

            if verbose and (batch_idx + 1) % 50 == 0:
                print(f"Val batch {batch_idx + 1}")
                print(f"Predictions: {torch.sigmoid(out[:3])}")
                print(f"Targets:     {y[:3]}")

    return total_loss / num_batches