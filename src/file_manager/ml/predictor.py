from __future__ import annotations

from pathlib import Path

from file_manager.ml.features import extract_image_features
from file_manager.ml.persistence import load_artifact


def predict_image_class(image_path: Path, model_dir: Path, image_size: tuple[int, int] = (128, 128)) -> dict[str, object]:
    model = load_artifact(model_dir / "image_classifier.joblib")
    encoder = load_artifact(model_dir / "label_encoder.joblib")
    features = extract_image_features(image_path, image_size).reshape(1, -1)
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    label = encoder.inverse_transform([prediction])[0]
    return {
        "predicted_label": label,
        "probabilities": {encoder.classes_[i]: float(probabilities[i]) for i in range(len(encoder.classes_))},
    }
