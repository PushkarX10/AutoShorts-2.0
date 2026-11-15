"""AutoShorts 2.0 - YouTube Auto Uploader Module
Uploads 9:16 vertical videos directly to YouTube Shorts using OAuth 2.0.
"""

import os
import sys
import pickle
from pathlib import Path
from typing import Dict, Any, Optional, List

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

class YouTubeUploader:
    def __init__(
        self,
        client_secrets_file: str = "client_secrets.json",
        token_file: str = "token.pickle"
    ):
        self.client_secrets_file = Path(client_secrets_file)
        self.token_file = Path(token_file)
        if not self.client_secrets_file.exists():
            raise FileNotFoundError(
                f"Missing '{self.client_secrets_file}'. Please place your Google OAuth desktop credentials JSON in the project root."
            )
        self.youtube = self._authenticate()

    def _authenticate(self):
        credentials = None
        # token.pickle stores the user's access & refresh tokens
        if self.token_file.exists():
            try:
                with open(self.token_file, "rb") as token:
                    credentials = pickle.load(token)
            except Exception as e:
                print(f"[AUTH WARNING] Could not read existing token: {e}")
                credentials = None

        # If there are no valid credentials, run the local auth flow
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                try:
                    credentials.refresh(Request())
                except Exception as e:
                    print(f"[AUTH REFRESH FAILED] {e}. Re-authenticating...")
                    credentials = None

            if not credentials:
                print("\n=======================================================")
                print("[YOUTUBE AUTH] Opening browser for one-time channel authorization...")
                print("Please log in with the Google account for your YouTube Channel.")
                print("=======================================================\n")
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.client_secrets_file), SCOPES
                )
                credentials = flow.run_local_server(port=0)

            # Save the credentials for headless future runs
            with open(self.token_file, "wb") as token:
                pickle.dump(credentials, token)
            print(f"[AUTH OK] Token saved to '{self.token_file}'. Future uploads will be automatic.")

        return build("youtube", "v3", credentials=credentials)

    def upload_short(
        self,
        video_path: str,
        title: str,
        description: str = "",
        tags: Optional[List[str]] = None,
        privacy_status: str = "private",
        thumbnail_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Uploads a video to YouTube with Shorts optimization.
        
        privacy_status: 'private', 'unlisted', or 'public'
        """
        video_file = Path(video_path)
        if not video_file.exists():
            raise FileNotFoundError(f"Video file not found: {video_file}")

        # Ensure #Shorts is in the title for automatic YouTube Shorts categorization
        clean_title = title.strip()
        if "#shorts" not in clean_title.lower():
            clean_title = f"{clean_title} #Shorts"
        clean_title = clean_title[:100]

        default_tags = ["Shorts", "History", "Documentary", "Facts", "Education"]
        merged_tags = list(dict.fromkeys((tags or []) + default_tags))

        full_description = f"{description.strip()}\n\n#Shorts #History #Documentary #Education".strip()

        body = {
            "snippet": {
                "title": clean_title,
                "description": full_description,
                "tags": merged_tags,
                "categoryId": "27"  # 27 = Education
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": False
            }
        }

        print(f"\n[YOUTUBE UPLOAD] Starting upload for: {video_file.name}")
        print(f"  Title: {clean_title}")
        print(f"  Privacy: {privacy_status}")

        media = MediaFileUpload(
            str(video_file),
            chunksize=1024 * 1024 * 4,  # 4MB chunks
            resumable=True,
            mimetype="video/mp4"
        )

        request = self.youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                print(f"  -> Upload progress: {progress}%", end="\r", flush=True)

        video_id = response.get("id")
        video_url = f"https://youtube.com/shorts/{video_id}"
        print(f"\n[OK] Video successfully uploaded!")
        print(f"  Video ID: {video_id}")
        print(f"  Watch URL: {video_url}")

        # Optional Thumbnail upload
        if thumbnail_path and Path(thumbnail_path).exists():
            try:
                print(f"  -> Uploading custom thumbnail: {Path(thumbnail_path).name}...")
                self.youtube.thumbnails().set(
                    videoId=video_id,
                    media_body=MediaFileUpload(str(thumbnail_path), mimetype="image/png")
                ).execute()
                print("  [OK] Custom thumbnail uploaded.")
            except Exception as e:
                print(f"  [NOTE] Thumbnail skipped (requires verified phone on channel): {e}")

        return {
            "video_id": video_id,
            "video_url": video_url,
            "title": clean_title,
            "privacy_status": privacy_status
        }

if __name__ == "__main__":
    # Test authentication standalone
    print("Testing YouTube Authentication...")
    uploader = YouTubeUploader()
    print("Authentication test successful!")
