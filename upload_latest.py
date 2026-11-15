"""AutoShorts 2.0 - Standalone YouTube Upload CLI
Uploads the latest generated YouTube Short to your channel.
"""

import sys
import json
import argparse
from pathlib import Path

from autoshorts2.uploader.youtube_uploader import YouTubeUploader

def main():
    parser = argparse.ArgumentParser(description="Upload YouTube Short from AutoShorts 2.0")
    parser.add_argument("--video", default="output/history_light_short.mp4", help="Path to video MP4 file")
    parser.add_argument("--package", default="output/history_light_package.json", help="Path to package JSON metadata")
    parser.add_argument("--thumbnail", default="output/history_light_thumbnail.png", help="Path to thumbnail PNG")
    parser.add_argument("--privacy", default="private", choices=["private", "unlisted", "public"], help="Privacy status")
    parser.add_argument("--title", default=None, help="Custom video title")
    args = parser.parse_args()

    video_path = Path(args.video)
    if not video_path.exists():
        print(f"[ERROR] Video file not found: {video_path}")
        sys.exit(1)

    title = args.title
    description = ""
    tags = ["Shorts", "History", "Julius Caesar", "Alesia", "Documentary"]

    pkg_path = Path(args.package)
    if pkg_path.exists():
        try:
            with open(pkg_path, "r", encoding="utf-8") as f:
                pkg_data = json.load(f)
            if not title:
                title = pkg_data.get("title", "How Julius Caesar Besieged the Besiegers at Alesia (52 BC)")
            description = pkg_data.get("full_script", "")
        except Exception as e:
            print(f"[WARNING] Could not read package json: {e}")

    if not title:
        title = "Caesar's Impossible Double Wall at Alesia (52 BC)"

    print("=======================================================")
    print("[AUTOSHORTS 2.0] YOUTUBE AUTO UPLOADER")
    print(f"Video File:     {video_path}")
    print(f"Title:          {title}")
    print(f"Privacy:        {args.privacy}")
    print(f"Thumbnail:      {args.thumbnail}")
    print("=======================================================\n")

    try:
        uploader = YouTubeUploader(client_secrets_file="client_secrets.json", token_file="token.pickle")
        res = uploader.upload_short(
            video_path=str(video_path),
            title=title,
            description=description,
            tags=tags,
            privacy_status=args.privacy,
            thumbnail_path=args.thumbnail if Path(args.thumbnail).exists() else None
        )
        print("\n=======================================================")
        print(f"SUCCESS: Video published at: {res['video_url']}")
        print("=======================================================")
    except Exception as e:
        print(f"\n[UPLOAD ERROR] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
