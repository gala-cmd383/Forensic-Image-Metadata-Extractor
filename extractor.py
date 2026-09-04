import hashlib
from pathlib import Path
import exifread
from PIL import Image, ExifTags
import pillow_heif

# Register HEIF opener for Pillow support
pillow_heif.register_heif_opener()


class ForensicImageExtractor:

    def __init__(self, image_path: str):
        self.image_path = Path(image_path.strip("\"'"))

    def calculate_sha256(self) -> str:
        sha256 = hashlib.sha256()
        with open(self.image_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()

    def _convert_to_degrees(self, ratio_list) -> float:
        try:
            d = float(ratio_list[0].num) / float(ratio_list[0].den)
            m = float(ratio_list[1].num) / float(ratio_list[1].den)
            s = float(ratio_list[2].num) / float(ratio_list[2].den)
            return d + (m / 60.0) + (s / 3600.0)
        except Exception:
            return 0.0

    def extract_metadata(self) -> dict:
        report = {
            "Filename": self.image_path.name,
            "SHA-256": self.calculate_sha256(),
            "Camera Info": {},
            "Timestamps": {},
            "GPS Info": {},
            "Google Maps Link": None,
        }

        tags = {}
        try:
            with open(self.image_path, "rb") as f:
                tags = exifread.process_file(f, details=True)
        except Exception:
            pass

        # Fallback to Pillow for HEIC and standard formats if exifread returns empty
        if not tags:
            try:
                with Image.open(self.image_path) as img:
                    raw_exif = img.getexif()
                    if raw_exif:
                        for tag_id, value in raw_exif.items():
                            tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                            tags[f"Image {tag_name}"] = value
            except Exception:
                pass

        if not tags:
            return report

        for key, tag_name in [
            ("Image Make", "Manufacturer"),
            ("Image Model", "Model"),
            ("Image Software", "Software/OS"),
        ]:
            if key in tags:
                report["Camera Info"][tag_name] = str(tags[key])

        timestamp = tags.get(
            "EXIF DateTimeOriginal", tags.get("Image DateTime", None)
        )
        if timestamp:
            report["Timestamps"]["Date/Time Captured"] = str(timestamp)

        gps_lat = tags.get("GPS GPSLatitude")
        gps_lat_ref = tags.get("GPS GPSLatitudeRef")
        gps_lon = tags.get("GPS GPSLongitude")
        gps_lon_ref = tags.get("GPS GPSLongitudeRef")

        if gps_lat and gps_lon and gps_lat_ref and gps_lon_ref:
            try:
                lat = self._convert_to_degrees(gps_lat.values)
                if str(gps_lat_ref).strip().upper() != "N":
                    lat = -lat

                lon = self._convert_to_degrees(gps_lon.values)
                if str(gps_lon_ref).strip().upper() != "E":
                    lon = -lon

                report["GPS Info"]["Latitude"] = round(lat, 6)
                report["GPS Info"]["Longitude"] = round(lon, 6)
                report["Google Maps Link"] = (
                    f"https://www.google.com/maps?q={lat},{lon}"
                )
            except Exception:
                pass

        return report


def main():
    print("=" * 50)
    print("      Forensic Image Metadata Extractor       ")
    print("=" * 50)

    user_input = input("Enter target image path: ").strip()

    if not user_input:
        print("[!] Error: No path provided.")
        return

    path_obj = Path(user_input.strip("\"'"))
    if not path_obj.exists():
        print(f"[!] Error: File '{user_input}' does not exist.")
        return

    print("\n[+] Extracting forensic evidence...\n")
    extractor = ForensicImageExtractor(user_input)
    data = extractor.extract_metadata()

    print(f"[*] File Name      : {data['Filename']}")
    print(f"[*] SHA-256 Hash   : {data['SHA-256']}\n")

    print("--- Camera & Device Details ---")
    if data["Camera Info"]:
        for k, v in data["Camera Info"].items():
            print(f"  • {k}: {v}")
    else:
        print("  • No camera details found.")

    print("\n--- Timestamps ---")
    if data["Timestamps"]:
        for k, v in data["Timestamps"].items():
            print(f"  • {k}: {v}")
    else:
        print("  • No EXIF timestamps found.")

    print("\n--- Geolocation Data (OSINT / Forensics) ---")
    if data["Google Maps Link"]:
        print(f"  • Latitude  : {data['GPS Info']['Latitude']}")
        print(f"  • Longitude : {data['GPS Info']['Longitude']}")
        print(f"  • Location  : {data['Google Maps Link']}")
    else:
        print("  • No GPS coordinates embedded in this image.")


if __name__ == "__main__":
    main()
