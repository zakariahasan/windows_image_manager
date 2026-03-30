from __future__ import annotations

from pathlib import Path

from file_manager.logging.logger import get_logger
from file_manager.operations.copier import copy_file
from file_manager.operations.duplicate_policy import DuplicateHandling
from file_manager.operations.mover import move_file
from file_manager.utils.csv_utils import read_csv_rows, write_csv_rows


app_logger = get_logger("app")
error_logger = get_logger("errors")


def apply_actions_from_csv(
    csv_path: Path,
    action: str,
    destination_dir: Path | None = None,
    policy: DuplicateHandling = DuplicateHandling.RENAME,
    dry_run: bool = False,
    output_csv_path: Path | None = None,
) -> Path:
    rows = read_csv_rows(csv_path)
    updated_rows: list[dict[str, object]] = []

    for row in rows:
        source = Path(row["full_path"])
        row["action_taken"] = action

        try:
            if not source.exists():
                row["action_status"] = "source-missing"
                row["remarks"] = "file not found at action time"
                updated_rows.append(row)
                continue

            if action == "copy":
                if destination_dir is None:
                    raise ValueError("destination_dir is required for copy")
                success, status, dest = copy_file(source, destination_dir, policy, dry_run=dry_run)
                row["action_status"] = "success" if success else "failed"
                row["remarks"] = status if dest is None else f"{status}: {dest}"
            elif action == "move":
                if destination_dir is None:
                    raise ValueError("destination_dir is required for move")
                success, status, dest = move_file(source, destination_dir, policy, dry_run=dry_run)
                row["action_status"] = "success" if success else "failed"
                row["remarks"] = status if dest is None else f"{status}: {dest}"
            elif action == "delete":
                if dry_run:
                    row["action_status"] = "success"
                    row["remarks"] = "dry-run-delete"
                else:
                    source.unlink()
                    row["action_status"] = "success"
                    row["remarks"] = "deleted"
            else:
                row["action_status"] = "failed"
                row["remarks"] = f"unsupported action: {action}"
        except Exception as exc:  # noqa: BLE001
            error_logger.exception("Failed CSV action for %s: %s", source, exc)
            row["action_status"] = "failed"
            row["remarks"] = str(exc)

        updated_rows.append(row)

    output_path = output_csv_path or csv_path
    write_csv_rows(updated_rows, output_path)
    app_logger.info("CSV action complete action=%s csv=%s output=%s", action, csv_path, output_path)
    return output_path
