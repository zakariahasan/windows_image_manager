from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Windows Image Manager Toolkit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan-images", help="Recursively scan images and export CSV")
    scan_parser.add_argument("--targets", nargs="+", required=True)
    scan_parser.add_argument("--extensions", nargs="*")
    scan_parser.add_argument("--output-csv", required=True)
    scan_parser.add_argument("--hash", action="store_true")
    scan_parser.add_argument("--checkpoint")

    dup_parser = subparsers.add_parser("duplicates", help="Find duplicate images")
    dup_parser.add_argument("--targets", nargs="+", required=True)
    dup_parser.add_argument("--extensions", nargs="*")
    dup_parser.add_argument("--checkpoint")

    copy_parser = subparsers.add_parser("copy-images", help="Copy scanned images directly")
    copy_parser.add_argument("--sources", nargs="+", required=True)
    copy_parser.add_argument("--destination", required=True)
    copy_parser.add_argument("--policy", default="rename", choices=["skip", "overwrite", "rename", "hash-compare-skip"])
    copy_parser.add_argument("--dry-run", action="store_true")

    move_parser = subparsers.add_parser("move-images", help="Move scanned images directly")
    move_parser.add_argument("--sources", nargs="+", required=True)
    move_parser.add_argument("--destination", required=True)
    move_parser.add_argument("--policy", default="rename", choices=["skip", "overwrite", "rename", "hash-compare-skip"])
    move_parser.add_argument("--dry-run", action="store_true")

    csv_action_parser = subparsers.add_parser("csv-action", help="Apply copy, move, or delete using CSV report")
    csv_action_parser.add_argument("--csv", required=True)
    csv_action_parser.add_argument("--action", required=True, choices=["copy", "move", "delete"])
    csv_action_parser.add_argument("--destination")
    csv_action_parser.add_argument("--policy", default="rename", choices=["skip", "overwrite", "rename", "hash-compare-skip"])
    csv_action_parser.add_argument("--dry-run", action="store_true")
    csv_action_parser.add_argument("--output-csv")

    zip_parser = subparsers.add_parser("zip", help="Create ZIP archive")
    zip_parser.add_argument("--sources", nargs="+", required=True)
    zip_parser.add_argument("--archive", required=True)
    zip_parser.add_argument("--password")

    send_parser = subparsers.add_parser("send", help="Send file over local network")
    send_parser.add_argument("--host", required=True)
    send_parser.add_argument("--port", type=int, required=True)
    send_parser.add_argument("--file", required=True)

    receive_parser = subparsers.add_parser("receive", help="Receive file over local network")
    receive_parser.add_argument("--bind-host", default="0.0.0.0")
    receive_parser.add_argument("--port", type=int, required=True)
    receive_parser.add_argument("--destination", required=True)

    train_parser = subparsers.add_parser("train-image-model", help="Train image classifier")
    train_parser.add_argument("--dataset", required=True)
    train_parser.add_argument("--model-dir", required=True)

    predict_parser = subparsers.add_parser("classify-image", help="Predict image class")
    predict_parser.add_argument("--image", required=True)
    predict_parser.add_argument("--model-dir", required=True)

    image_info_parser = subparsers.add_parser("image-info", help="Inspect an image")
    image_info_parser.add_argument("--image", required=True)

    return parser
