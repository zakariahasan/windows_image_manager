from __future__ import annotations

from pathlib import Path
from pprint import pprint

from file_manager.archive.zipper import create_zip_archive
from file_manager.cli.parser import build_parser
from file_manager.config.loader import load_settings
from file_manager.image_utils.inspector import get_image_info, read_exif
from file_manager.logging.logger import setup_logging
from file_manager.ml.predictor import predict_image_class
from file_manager.ml.trainer import train_image_classifier
from file_manager.operations.copier import copy_file
from file_manager.operations.csv_actions import apply_actions_from_csv
from file_manager.operations.duplicate_policy import DuplicateHandling
from file_manager.operations.mover import move_file
from file_manager.scanner.scanner import ImageScanner
from file_manager.transfer.receiver import receive_once
from file_manager.transfer.sender import send_file
from file_manager.utils.csv_utils import export_records_to_csv


def run_cli() -> None:
    settings = load_settings()
    setup_logging(settings)
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "scan-images":
        scanner = ImageScanner(compute_hash=args.hash)
        records = list(
            scanner.scan(
                [Path(t) for t in args.targets],
                args.extensions,
                checkpoint_path=Path(args.checkpoint) if args.checkpoint else None,
            )
        )
        export_records_to_csv(records, Path(args.output_csv))
        print(f"Scanned {len(records)} image(s). CSV exported to {args.output_csv}")
        return

    if args.command == "duplicates":
        from file_manager.duplicates.detector import DuplicateDetector

        scanner = ImageScanner(compute_hash=False)
        records = list(
            scanner.scan(
                [Path(t) for t in args.targets],
                args.extensions,
                checkpoint_path=Path(args.checkpoint) if args.checkpoint else None,
            )
        )
        detector = DuplicateDetector()
        groups = detector.find_duplicates([record.full_path for record in records if record.is_valid_image])
        for group in groups:
            print(f"{group.group_id} | {group.hash_value} | {len(group.files)} files")
            for file_path in group.files:
                print(f"  - {file_path}")
        return

    if args.command == "copy-images":
        for source in [Path(s) for s in args.sources]:
            success, status, destination = copy_file(
                source,
                Path(args.destination),
                DuplicateHandling(args.policy),
                dry_run=args.dry_run,
            )
            print(success, status, destination)
        return

    if args.command == "move-images":
        for source in [Path(s) for s in args.sources]:
            success, status, destination = move_file(
                source,
                Path(args.destination),
                DuplicateHandling(args.policy),
                dry_run=args.dry_run,
            )
            print(success, status, destination)
        return

    if args.command == "csv-action":
        result_csv = apply_actions_from_csv(
            csv_path=Path(args.csv),
            action=args.action,
            destination_dir=Path(args.destination) if args.destination else None,
            policy=DuplicateHandling(args.policy),
            dry_run=args.dry_run,
            output_csv_path=Path(args.output_csv) if args.output_csv else None,
        )
        print(f"CSV action completed. Updated report: {result_csv}")
        return

    if args.command == "zip":
        archive = create_zip_archive([Path(s) for s in args.sources], Path(args.archive), args.password)
        print(f"Archive created: {archive}")
        return

    if args.command == "send":
        send_file(args.host, args.port, Path(args.file))
        print("File sent successfully")
        return

    if args.command == "receive":
        output = receive_once(args.bind_host, args.port, Path(args.destination))
        print(f"Received file: {output}")
        return

    if args.command == "train-image-model":
        result = train_image_classifier(Path(args.dataset), Path(args.model_dir))
        pprint(result)
        return

    if args.command == "classify-image":
        result = predict_image_class(Path(args.image), Path(args.model_dir))
        pprint(result)
        return

    if args.command == "image-info":
        info = get_image_info(Path(args.image))
        exif = read_exif(Path(args.image))
        pprint(info)
        pprint(exif)
        return
