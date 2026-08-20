# Forensic Image Metadata Extractor 🔍📸

A modular Python tool designed for **Digital Forensics Investigators**, **Incident Responders**, and **OSINT Analysts** to extract hidden EXIF metadata, verify digital evidence integrity, and parse geolocation coordinates from digital media.

---

## 🌟 Key Features

* **Evidence Integrity & Chain of Custody:** Computes **SHA-256 cryptographic hashes** to ensure evidence has not been tampered with or modified.
* **Camera & Device Attribution:** Extracts manufacturer, camera/smartphone model, lens configuration, and software/OS versions.
* **Timestamp Extraction:** Retrieves original creation timestamps (`DateTimeOriginal`) and digitization metadata.
* **GPS & Geolocation Resolution:** Decodes raw degree/minute/second EXIF tags into decimal coordinates and generates direct **Google Maps** investigation links.
* **Cross-Format Compatibility:** Fully supports modern Apple **HEIC/HEIF** formats alongside standard **JPEG/JPG/PNG** media.

---

## 🛠️ Architecture & Workflow

```text
[Target Image (JPG/HEIC/PNG)]
          │
          ├──► SHA-256 Hashing ──────────► Forensic Integrity Check
          │
          └──► EXIF Header Parsing
                    ├──► Device Hardware & OS Metadata
                    ├──► Timestamps & Creation Dates
                    └──► GPS Coordinates ──► Decimal Conversion ──► Google Maps
```
## Installation & Usage
* **Clone the Repository** git clone [https://github.com/gala-cmd383/Forensic-Image-Metadata-Extractor.git](https://github.com/gala-cmd383/Forensic-Image-Metadata-Extractor.git)
cd Forensic-Image-Metadata-Extractor
* **Install Dependencies** pip install -r requirements.txt
* **Run the Analyzer** python extractor.py
## 📊 Sample Output


```text
==================================================
      Forensic Image Metadata Extractor       
==================================================
Enter target image path: IMG_1915.HEIC

[+] Extracting forensic evidence...

[*] File Name      : IMG_1915.HEIC
[*] SHA-256 Hash   : bd7502d283c731d08bc329adbb4bf5fdd335e2650f6768b427e28c7be59bfee6

--- Camera & Device Details ---
  • Manufacturer : Apple
  • Model        : iPhone 14 Pro
  • Software/OS  : 17.4.1

--- Timestamps ---
  • Date/Time Captured : 2026:08:20 20:35:12

--- Geolocation Data (OSINT / Forensics) ---
  • Latitude  : 24.713552
  • Longitude : 46.675296
  • Location  : [https://www.google.com/maps?q=24.713552,46.675296](https://www.google.com/maps?q=24.713552,46.675296)
```
##📄 License
* **This project is licensed under the MIT License - see the LICENSE file for details**
