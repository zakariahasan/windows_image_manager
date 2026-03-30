# 🖼️ Windows Image Manager Toolkit

A modular, production-style Python project for scanning, managing, and processing images on Windows.

---
## Project layout

```text
windows_file_manager/
│
├── main.py
├── README.md
├── requirements.txt
├── .env.example
│
├── src/
│ └── file_manager/
│ ├── cli/
│ ├── scanner/
│ ├── operations/
│ ├── duplicates/
│ ├── archive/
│ ├── transfer/
│ ├── image_utils/
│ ├── ml/
│ ├── utils/
│ ├── models/
│ ├── config/
│ ├── logging/
│ └── services/
│
└── tests/
```
# 🚀 Features

## 🔍 Image Scanning
- Recursively scan full drives or directories
- Filter by image types (.jpg, .png, etc.)
- Extract metadata (size, resolution, format, mode)
- Optional hashing for duplicate detection
- Export results to CSV

## 🔁 Resume / Checkpoint (Watermark)
- Automatically saves scan progress
- Resume scan after failure or interruption

## 📊 CSV-Based Workflow
- CSV acts as a source of truth
- Perform actions using CSV: copy, move, delete
- Tracks action status in CSV

## 📦 File Operations
- Copy or move files with duplicate handling:
  skip, overwrite, rename, hash-compare-skip

## 🧠 Duplicate Detection
- Detect duplicates by content (hash-based)

## 🗜️ Archiving
- ZIP files with optional password

## 🌐 Local Network Transfer
- Send/receive files over LAN

## 🧠 Machine Learning
- Train and classify images

## 📜 Logging
- app.log, scan.log, errors.log

---

# ⚙️ Setup

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
$env:PYTHONPATH="src"
```

---

# 📂 Create Directories

```powershell
mkdir output
mkdir output\checkpoints
mkdir logs
mkdir output\archives
```

---

# 🔍 Scan Images

```powershell
python main.py scan-images `
  --targets C:\pic `
  --extensions .jpg .png `
  --output-csv output\scan_results.csv `
  --hash `
  --checkpoint output\checkpoints\scan_progress.json
```

---

# 🔁 Resume Scan

Re-run same command to resume.

---

# 📄 CSV Actions

## Copy
```powershell
python main.py csv-action `
  --csv output\scan_results.csv `
  --action copy `
  --destination D:\reviewed `
  --output-csv output\copy_results.csv
```

## Move
```powershell
python main.py csv-action `
  --csv output\scan_results.csv `
  --action move `
  --destination D:\archive `
  --output-csv output\move_results.csv
```

## Delete
```powershell
python main.py csv-action `
  --csv output\scan_results.csv `
  --action delete `
  --output-csv output\delete_results.csv
```

## Dry Run
```powershell
python main.py csv-action `
  --csv output\scan_results.csv `
  --action move `
  --destination D:\archive `
  --dry-run `
  --output-csv output\dry_run.csv
```

---

# 🗜️ Archive

```powershell
python main.py zip --sources C:\pic\a.jpg --archive output\archives\images.zip
```

---

# 🌐 Transfer

## Receive
```powershell
python main.py receive --port 9000 --destination D:\incoming
```

## Send
```powershell
python main.py send --host 192.168.1.10 --port 9000 --file C:\pic\a.jpg
```

---

# 🧠 Image Info

```powershell
python main.py image-info --image C:\pic\a.jpg
```

---

# 🤖 ML

## Train
```powershell
python main.py train-image-model --dataset dataset\images --model-dir models\
```

## Predict
```powershell
python main.py classify-image --image C:\pic\test.jpg --model-dir models\
```

---

# 📜 Logs

```powershell
Get-Content logs\errors.log -Tail 50
```

---

# ⚠️ Troubleshooting

## Fix import error
```powershell
$env:PYTHONPATH="src"
```

## Slow scan
- Disable hash if not needed

## Permission issues
- Run PowerShell as admin

---

# 📈 Workflow

Scan → Review CSV → Detect duplicates → Dry-run → Execute → Verify

---

# 🧠 Mental Model

Scan → Describe → Resume → Decide → Act → Verify

## Updated ZIP behavior

The `zip` command now supports:
- recursive directory archiving
- optional password protection
- detailed archive logging
- optional `--images-only` filtering when source paths are directories

### Zip an entire folder recursively
```powershell
python main.py zip --sources C:\pic1 --archive output\archives\images.zip
```

### Zip only image files from a folder recursively
```powershell
python main.py zip --sources C:\pic1 --archive output\archives\images_only.zip --images-only
```

### Zip recursively with password protection
```powershell
python main.py zip --sources C:\pic1 --archive output\archives\secure_images.zip --password mysecret
```

### Archive logging
```powershell
Get-Content logs\archive.log -Tail 50
```

Notes:
- If `pyzipper` is installed, password protection uses AES encryption.
- If `pyzipper` is not available, the tool falls back to standard ZIP creation without password protection and logs a warning.