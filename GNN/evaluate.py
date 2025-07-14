import torch
import json
from tqdm import tqdm

def evaluate_and_save_predictions(dataset, model, device, output_path="val_predictions.json"):
    model.eval()
    predictions = {}

    total_correct = 0
    total_preds = 0

    with torch.no_grad():
        for idx, snapshot in enumerate(tqdm(dataset)):
            snapshot.to(device)

            out = model(snapshot.x, snapshot.edge_index, snapshot.edge_attr)
            probs = torch.sigmoid(out)
            preds = (probs > 0.5).long()

            targets = snapshot.y.long()

            correct = (preds == targets).sum().item()
            total = targets.numel()
            acc = correct / total

            total_correct += correct
            total_preds += total

            predictions[f"frame_{idx}"] = {
                "probabilities": probs.cpu().tolist(),
                "predictions": preds.cpu().tolist(),
                "targets": targets.cpu().tolist(),
                "frame_accuracy": round(acc, 3),
            }

    overall_accuracy = round(total_correct / total_preds, 3)

    with open(output_path, "w") as f:
        json.dump(predictions, f, indent=2)

    print(f"Accuracy: {overall_accuracy:.4f}")