import os
import shutil
import time
import argparse
import logging
import hashlib
import zipfile
from cryptography.fernet import Fernet
import pandas as pd
from datetime import datetime

def calculate_hash(filename, algorithm="sha256"):

  hasher = hashlib.new(algorithm)
  with open(filename, "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
      hasher.update(chunk)
  return hasher.hexdigest()


def compress_directory(directory, output_dir):

  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  archive_name = os.path.join(output_dir, f"{os.path.basename(directory)}.zip")
  with zipfile.ZipFile(archive_name, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for root, dirs, files in os.walk(directory):
      for file in files:
        archive.write(os.path.join(root, file))
  return archive_name


def encrypt_file(filename, key, output_dir):
  
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  cipher = Fernet(key)
  with open(filename, "rb") as f:
    data = f.read()
  ciphertext = cipher.encrypt(data)

  encrypted_filename = os.path.join(output_dir, f"{os.path.basename(filename)}.enc")
  with open(encrypted_filename, "wb") as f:
    f.write(ciphertext)
  return encrypted_filename

def create_report(evidence_files, output_dir):

  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  report = pd.DataFrame(evidence_files)
  report_name = os.path.join(output_dir, "evidence_report.csv")
  report.to_csv(report_name, index=False)
  return report_name

def main():
  
  parser = argparse.ArgumentParser(description="Windows Evidence Collection Script")
  parser.add_argument("machine_name", help="Name of the machine")
  parser.add_argument("evidence_dir", help="Directory containing the evidence")
  parser.add_argument("-k", "--key", help="Fernet encryption key")
  parser.add_argument("-o", "--output_dir", default="output", help="Output directory for processed files")
  args = parser.parse_args()

  if not os.path.exists(args.evidence_dir):
    raise ValueError(f"Evidence directory not found: {args.evidence_dir}")

logging.basicConfig(
      format="%(asctime)s %(levelname)-8s %(message)s",
      level=logging.INFO,
      filename=f"{args.machine_name}_log.txt"
  )

  evidence_files = []

  for root, dirs, files in os.walk(args.evidence_dir):
    for file in files:
      filename = os.path.join(root, file)
      size = os.path.getsize(filename)
      timestamp = os.path.getmtime(filename)
      file_hash = calculate_hash(filename)

      evidence_files.append({
          "filename": filename,
          "size": size,
          "timestamp": datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
          "hash": file_hash
      })

  compressed_file = compress_directory(args.evidence_dir, args.output_dir)
  encrypted_file = encrypt_file(compressed_file, args.key, args.output_dir)

  report_name = create_report(evidence_files, args.output_dir)

  logging.info("Evidence collected and processed successfully!")
  logging.info(f"Report saved to: {report_name}")
  logging.info(f"Compressed and encrypted archive: {encrypted_file}")

if __name__ == "__main__":
  main()
