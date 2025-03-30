#%% Imports
from ultralytics import YOLO
# from codecarbon import OfflineEmissionsTracker  
import torch
import os

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"using : {device}")


#%% Functions

# @codecarbone_fr
def train_yolo(*, model: str, dataset_path: str, batch_size: int, epochs: int):
    yolo = YOLO(model)

    # Train the model
    metrics = yolo.train(data=dataset_path, imgsz=640, batch=batch_size, epochs=epochs, device=device,lr0=0.005)

    if metrics is not None:
        print("Metrics: ", metrics)

    return yolo


def main():
    model_name = "yolo11m-obb.pt"
    # train_path = '/kaggle/input/book-spine/data.yaml'
    train_path = '../data/dataset_YoloV8obb/data.yaml'

    model = train_yolo(model=model_name, dataset_path=train_path, batch_size=16, epochs=100)

    
    return


#%% Call main
if __name__ == "__main__":
    main()
