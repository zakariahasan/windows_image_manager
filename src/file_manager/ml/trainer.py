from __future__ import annotations

from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from file_manager.logging.logger import get_logger
from file_manager.ml.dataset import discover_labeled_images
from file_manager.ml.features import extract_image_features
from file_manager.ml.persistence import save_artifact


ml_logger = get_logger("ml")


def train_image_classifier(
    dataset_root: Path,
    model_output_dir: Path,
    image_size: tuple[int, int] = (128, 128),
    test_size: float = 0.2,
    random_state: int = 42,
) -> dict[str, object]:
    samples = discover_labeled_images(dataset_root)
    if not samples:
        raise ValueError("No labeled images found in dataset")

    features = []
    labels = []
    for path, label in samples:
        try:
            features.append(extract_image_features(path, image_size))
            labels.append(label)
        except Exception as exc:  # noqa: BLE001
            ml_logger.warning("Skipping invalid training image %s: %s", path, exc)

    X = np.vstack(features)
    y = np.array(labels)

    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y_encoded,
        test_size=test_size,
        random_state=random_state,
        stratify=y_encoded,
    )

    model = RandomForestClassifier(n_estimators=200, random_state=random_state, n_jobs=-1)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    report = classification_report(y_test, predictions, target_names=encoder.classes_, output_dict=True)
    matrix = confusion_matrix(y_test, predictions).tolist()

    save_artifact(model, model_output_dir / "image_classifier.joblib")
    save_artifact(encoder, model_output_dir / "label_encoder.joblib")

    ml_logger.info("Training complete. Classes=%s", list(encoder.classes_))

    return {
        "classes": list(encoder.classes_),
        "classification_report": report,
        "confusion_matrix": matrix,
        "sample_count": len(features),
    }
