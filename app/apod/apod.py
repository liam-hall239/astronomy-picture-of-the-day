import argparse
import json
from pathlib import Path
from urllib.request import urlopen


def download_apod(output_dir):
	endpoint = "https://science.nasa.gov/wp-json/wp/v2/apod-basic"
	with urlopen(endpoint, timeout=60) as response:
		entry = json.load(response)[0]

	picture_dir = output_dir / "picture"
	json_dir = output_dir / "json"
	picture_dir.mkdir(parents=True, exist_ok=True)
	json_dir.mkdir(parents=True, exist_ok=True)
	if entry["media_type"] == "image":
		image_url = entry.get("hdurl")
		if not image_url:
			raise RuntimeError("APOD has no image download URL")
		destination = picture_dir / "apod.png"
		temporary = picture_dir / "apod.png.part"
		try:
			with urlopen(image_url, timeout=120) as response:
				if not response.headers.get_content_type().startswith("image/"):
					raise RuntimeError("APOD download did not return an image")
				temporary.write_bytes(response.read())
			temporary.replace(destination)
		finally:
			temporary.unlink(missing_ok=True)
		print(f"Saved {destination}")
	else:
		print(f"APOD is {entry['media_type']}; keeping the previous wallpaper")

	metadata = json_dir / "apod.json"
	temporary = json_dir / "apod.json.part"
	try:
		temporary.write_text(json.dumps(entry, indent=2) + "\n", encoding="utf-8")
		temporary.replace(metadata)
	finally:
		temporary.unlink(missing_ok=True)


def main():
	parser = argparse.ArgumentParser(description="Update the APOD wallpaper")
	parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parents[2] / "output")
	args = parser.parse_args()
	download_apod(args.output_dir)


if __name__ == "__main__":
	main()
