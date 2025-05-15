# Nuscenes Dataset Download (Enhanced Version)

A modified script for downloading and extracting the full nuScenes dataset, based on [li-xl/nuscenes-download](https://github.com/li-xl/nuscenes-download).
---

### What's New

- Logs in **before each file download** to prevent token expiration   
- Automatically **extracts and removes** archives after download
- Checks for **minimum disk space** before downloading
---

### Usage

1. Register and log in at [nuScenes.org](https://www.nuscenes.org/nuscenes)

2. Install dependencies:
   ```bash
   pip install requests tqdm
   ```
   - `requests`: handles login and download  
   - `tqdm`: shows download progress bars  

3. Configure the script:
   ```python
   USER_EMAIL = "your_email"
   USER_PASSWORD = "your_password"
   OUTPUT_DIR = "/path/to/save"
   REGION = "asia"  # or 'us'
   MIN_FREE_GB = 150  # Minimum free GB to continue
   ```

4. Run it:
   ```bash
   python download_nuscenes_dataset.py
   ```

---

### Acknowledgements

- Based on: [li-xl/nuscenes-download](https://github.com/li-xl/nuscenes-download)  
