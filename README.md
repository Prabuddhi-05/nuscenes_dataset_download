# Nuscenes Download (Enhanced Version)

**A modified script for downloading and extracting the full nuScenes dataset, based on [li-xl/nuscenes-download](https://github.com/li-xl/nuscenes-download).**

This version adds login automation, file integrity checks, and usability improvements. Please use responsibly for educational and research purposes only.

---

### What's New

- Added `trainval01–03` blobs for full dataset coverage  
- Logs in **before each file download** to prevent token expiration  
- Verifies file integrity using **MD5 checksums**  
- Checks for **minimum disk space** before downloading  
- Automatically **extracts and removes** archives after download  
- **Progress bar** added using `tqdm` for real-time download visibility

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
   ```

4. Run it:
   ```bash
   python download_nuscenes.py
   ```

---

### Acknowledgements

- Based on: [li-xl/nuscenes-download](https://github.com/li-xl/nuscenes-download)  
- Inspired by: [Syzygianinfern0/NuPlan-Download-CLI](https://github.com/Syzygianinfern0/NuPlan-Download-CLI)  
- Improvements from: [songshiyu01](https://github.com/songshiyu01), [harsanyidani](https://github.com/harsanyidani)
