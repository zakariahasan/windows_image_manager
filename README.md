# Windows File Manager Toolkit

## Overview

This is a modular Python project for:
- filesystem scanning
- metadata export to CSV
- duplicate detection by content hash
- copy/move with duplicate handling
- ZIP creation with optional password protection
- local network file transfer
- image inspection and processing
- image ML training and inference

## Project layout

```text
windows_file_manager/
├── README.md
├── requirements.txt
├── .env.example
├── main.py
├── pyproject.toml
├── src/
│   └── file_manager/
│       ├── config/
│       ├── logging/
│       ├── models/
│       ├── utils/
│       ├── scanner/
│       ├── duplicates/
│       ├── operations/
│       ├── archive/
│       ├── transfer/
│       ├── image_utils/
│       ├── ml/
│       ├── cli/
│       └── services/
└── tests/
```

## Setup

### 1. Create virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set environment variables

Copy `.env.example` to `.env` and edit as needed.

## Usage examples

### Scan files and export CSV

```bash
python main.py scan --targets C:\Users\YourName\Downloads D:\Data --extensions .jpg .png .pdf --output-csv output\scan_results.csv --hash
```

### Find duplicates

```bash
python main.py duplicates --targets C:\Users\YourName\Downloads --extensions .jpg .png
```

### Copy files

```bash
python main.py copy --sources C:\Temp\a.txt C:\Temp\b.txt --destination D:\Collected --policy rename
```

### Move files

```bash
python main.py move --sources C:\Temp\a.txt --destination D:\Archive --policy hash-compare-skip
```

### Create zip archive

```bash
python main.py zip --sources C:\Temp\a.txt C:\Temp\b.txt --archive output\archives\backup.zip --password mysecret
```

### Receive file on one machine

```bash
python main.py receive --bind-host 0.0.0.0 --port 50505 --destination D:\Incoming
```

### Send file from another machine

```bash
python main.py send --host 192.168.1.50 --port 50505 --file C:\Temp\photo.jpg
```

### Train image classifier

Dataset layout:

```text
dataset/
├── cats/
│   ├── img1.jpg
│   ├── img2.jpg
├── dogs/
│   ├── img3.jpg
│   ├── img4.jpg
```

Train:

```bash
python main.py train-image-model --dataset dataset --model-dir models
```

### Predict image class

```bash
python main.py classify-image --image sample.jpg --model-dir models
```

### Inspect image metadata

```bash
python main.py image-info --image sample.jpg
```

## Duplicate handling behavior

Supported policies:
- `skip`
- `overwrite`
- `rename`
- `hash-compare-skip`

## Password-protected ZIP notes

Standard Python `zipfile` does not provide strong modern encryption for writing password-protected ZIPs.
This project uses `pyzipper` when available. If `pyzipper` is missing, the project falls back to standard ZIP creation without password protection.

## Logging

Logs are written to:
- `logs/app.log`
- `logs/scan.log`
- `logs/duplicates.log`
- `logs/transfer.log`
- `logs/ml.log`
- `logs/archive.log`
- `logs/errors.log`

## Testing

Run:

```bash
pytest
```

## Future improvements

- store metadata in SQLite or PostgreSQL
- multithreaded scanning
- resumable transfers with manifest files
- TLS-encrypted transfer
- GUI frontend
- FastAPI backend
- deeper image similarity search using embeddings
- OCR integration
