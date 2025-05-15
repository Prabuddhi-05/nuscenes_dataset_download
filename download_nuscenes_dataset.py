```python
#!/usr/bin/env python3
import requests
import os
import hashlib
import shutil
from tqdm import tqdm
import tarfile
import gzip
import json
import time

# ─────────── USER CONFIG ───────────
USER_EMAIL = "your_email
USER_PASSWORD = "your_password"
OUTPUT_DIR = "/path/to/save"
REGION = "asia"  # or 'us'
MIN_FREE_GB = 150  # Minimum free GB to continue
# ──────────────────────────────────

# Files to download and their MD5 hashes
DOWNLOAD_FILES = {
    "v1.0-trainval01_blobs.tgz": "cbf32d2ea6996fc599b32f724e7ce8f2",
    "v1.0-trainval02_blobs.tgz": "aeecea4878ec3831d316b382bb2f72da",
    "v1.0-trainval03_blobs.tgz": "595c29528351060f94c935e3aaf7b995",
    "v1.0-trainval04_blobs.tgz": "b55eae9b4aa786b478858a3fc92fb72d",
    "v1.0-trainval05_blobs.tgz": "1c815ed607a11be7446dcd4ba0e71ed0",
    "v1.0-trainval06_blobs.tgz": "7273eeea36e712be290472859063a678",
    "v1.0-trainval07_blobs.tgz": "46674d2b2b852b7a857d2c9a87fc755f",
    "v1.0-trainval08_blobs.tgz": "37524bd4edee2ab99678909334313adf",
    "v1.0-trainval09_blobs.tgz": "a7fcd6d9c0934e4052005aa0b84615c0",
    "v1.0-trainval10_blobs.tgz": "31e795f2c13f62533c727119b822d739",
    "v1.0-test_meta.tgz": "b0263f5c41b780a5a10ede2da99539eb",
    "v1.0-test_blobs.tgz": "e065445b6019ecc15c70ad9d99c47b33",
}

def login(email: str, password: str) -> str:
    """Perform AWS Cognito login and return bearer token."""
    resp = requests.post(
        "https://cognito-idp.us-east-1.amazonaws.com/",
        headers={
            "Content-Type": "application/x-amz-json-1.1",
            "X-Amz-Target": "AWSCognitoIdentityProviderService.InitiateAuth",
        },
        data=json.dumps({
            "AuthFlow": "USER_PASSWORD_AUTH",
            "ClientId": "7fq5jvs5ffs1c50hd3toobb3b9",
            "AuthParameters": {"USERNAME": email, "PASSWORD": password}
        }),
    )
    resp.raise_for_status()
    return resp.json()["AuthenticationResult"]["IdToken"]

def check_and_warn_space(path: str):
    """Check free disk space and warn if below threshold."""
    total, used, free = shutil.disk_usage(path)
    free_gb = free // (1024**3)
    print(f"Disk space at {path}: {free_gb} GB free / {total // (1024**3)} GB total\n")
    if free_gb < MIN_FREE_GB:
        print(f"WARNING: Only {free_gb} GB free. Pausing for you to free up space...")
        input("Press Enter to continue when space is available...")

def download_and_check(url: str, dest: str, expected_md5: str):
    """Download file from URL and verify MD5 hash."""
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.exists(dest):
        with open(dest, 'rb') as f:
            file_md5 = hashlib.md5(f.read()).hexdigest()
        if file_md5 == expected_md5:
            print(f"[SKIP] {os.path.basename(dest)} already exists and MD5 checks out")
            return dest
        else:
            print(f"[RE-DOWNLOAD] {os.path.basename(dest)} MD5 mismatch, redownloading")

    # Stream download with progress bar
    r = requests.get(url, stream=True)
    r.raise_for_status()
    total = int(r.headers.get("Content-Length", "0"))
    with open(dest, "wb") as f, tqdm(total=total, unit="B", unit_scale=True, desc=os.path.basename(dest)) as pbar:
        md5obj = hashlib.md5()
        for chunk in r.iter_content(1024 * 32):
            if not chunk:
                break
            f.write(chunk)
            md5obj.update(chunk)
            pbar.update(len(chunk))

    got_md5 = md5obj.hexdigest()
    if got_md5 != expected_md5:
        raise ValueError(f"MD5 mismatch for {dest}: got {got_md5}, expected {expected_md5}")
    check_and_warn_space(os.path.dirname(dest))
    return dest

def extract(path: str):
    """Extract .tgz or .tar file and remove the archive after extraction."""
    print(f"⏳ Extracting {os.path.basename(path)} …")
    if path.endswith(".tgz"):
        with gzip.open(path, "rb") as gz, tarfile.open(fileobj=gz) as tar:
            tar.extractall(os.path.dirname(path))
    else:
        with tarfile.open(path, "r") as tar:
            tar.extractall(os.path.dirname(path))
    os.remove(path)
    print(f"Extracted and removed {os.path.basename(path)}")
    check_and_warn_space(os.path.dirname(path))

def main():
    """Main download and extract loop."""
    for fname, md5 in DOWNLOAD_FILES.items():
        print(f"\nLogging in before downloading {fname}")
        token = login(USER_EMAIL, USER_PASSWORD)
        headers = {"Authorization": f"Bearer {token}"}

        api = f"https://o9k5xn5546.execute-api.us-east-1.amazonaws.com/v1/archives/v1.0/{fname}?region={REGION}&project=nuScenes"
        print(f"📡 Requesting URL for: {fname}")
        resp = requests.get(api, headers=headers)
        if resp.status_code != 200:
            print(f"Failed to get URL for {fname}: {resp.status_code} - {resp.text}")
            continue

        url = resp.json()["url"]
        out_path = os.path.join(OUTPUT_DIR, fname)
        try:
            arc = download_and_check(url, out_path, md5)
            extract(arc)
        except Exception as e:
            print(f"Error while processing {fname}: {e}")
            continue

    print("\nAll selected nuScenes files processed successfully.")

if __name__ == "__main__":
    main()

