from __future__ import annotations

from pathlib import Path

from file_manager.ml.predictor import predict_image_class
from file_manager.ml.trainer import train_image_classifier


class MlService:
    def train(self, dataset_root: Path, model_dir: Path) -> dict[str, object]:
        return train_image_classifier(dataset_root, model_dir)

    def predict(self, image_path: Path, model_dir: Path) -> dict[str, object]:
        return predict_image_class(image_path, model_dir)
