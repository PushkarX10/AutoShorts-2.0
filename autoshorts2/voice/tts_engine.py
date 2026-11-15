"""Neural Voice Generation and Robust Word-Level Alignment Engine for AutoShorts 2.0
"""

import asyncio
import re
import subprocess
from pathlib import Path
from typing import List, Tuple, Dict, Any
import edge_tts
from autoshorts2.models import SubtitleWord
from autoshorts2.config import DEFAULT_VOICE

EMPHASIS_KEYWORDS = {
    "coins", "free", "dollar", "dollars", "million", "loophole", "cashback", "secret", "bank",
    "treasury", "mint", "boxes", "pallets", "illegal", "investigation", "never",
    "glitch", "zero", "$300,000", "$6,000", "$5,000", "$10,000", "$50,000", "$1.00",
    "100%", "closed", "rules", "warning", "federal", "banned", "profit", "watched",
    "caught", "spread", "math", "risk", "wild", "kept", "broken"
}

class TTSEngine:
    def __init__(self, voice: str = DEFAULT_VOICE, rate: str = "+3%"):
        self.voice = voice
        self.rate = rate

    async def synthesize(self, text: str, output_path: Path) -> Tuple[float, List[SubtitleWord]]:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        communicate = edge_tts.Communicate(text, self.voice, rate=self.rate)
        
        sentence_boundaries: List[Dict[str, Any]] = []
        raw_words: List[Dict[str, Any]] = []
        audio_bytes = bytearray()
        
        async for chunk in communicate.stream():
            ctype = chunk.get("type")
            if ctype == "audio":
                audio_bytes.extend(chunk["data"])
            elif ctype == "SentenceBoundary":
                start_s = chunk["offset"] / 10_000_000.0
                dur_s = chunk["duration"] / 10_000_000.0
                sentence_boundaries.append({
                    "text": chunk["text"],
                    "start": round(start_s, 3),
                    "duration": round(dur_s, 3),
                    "end": round(start_s + dur_s, 3)
                })
            elif ctype == "WordBoundary":
                start_s = chunk["offset"] / 10_000_000.0
                dur_s = chunk["duration"] / 10_000_000.0
                raw_words.append({
                    "word": chunk["text"],
                    "start": round(start_s, 3),
                    "end": round(start_s + dur_s, 3)
                })
                
        with open(output_path, "wb") as f:
            f.write(audio_bytes)

        # Get exact audio duration via ffprobe
        total_duration = 0.0
        try:
            cmd = [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1", str(output_path)
            ]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            total_duration = float(res.stdout.strip())
        except Exception:
            if sentence_boundaries:
                total_duration = sentence_boundaries[-1]["end"] + 0.3
            else:
                total_duration = max(10.0, len(text.split()) * 0.4)

        subtitle_words: List[SubtitleWord] = []

        # Strategy 1: Use raw words from edge_tts if available
        if raw_words:
            for rw in raw_words:
                clean_w = rw["word"].strip()
                if clean_w:
                    subtitle_words.append(SubtitleWord(
                        word=clean_w,
                        start=rw["start"],
                        end=rw["end"],
                        is_emphasized=self._check_emphasis(clean_w)
                    ))

        # Strategy 2: If raw words empty, use proportional distribution over SentenceBoundaries
        if not subtitle_words and sentence_boundaries:
            for sb in sentence_boundaries:
                s_words = sb["text"].strip().split()
                if not s_words:
                    continue
                s_start = sb["start"]
                s_end = sb["end"]
                s_dur = max(0.2, s_end - s_start)
                
                # Weight by word length
                total_chars = sum(max(1, len(w)) for w in s_words)
                curr_w_start = s_start
                for w in s_words:
                    w_fraction = max(1, len(w)) / total_chars
                    w_dur = s_dur * w_fraction
                    w_end = min(s_end, curr_w_start + w_dur)
                    subtitle_words.append(SubtitleWord(
                        word=w,
                        start=round(curr_w_start, 3),
                        end=round(w_end, 3),
                        is_emphasized=self._check_emphasis(w)
                    ))
                    curr_w_start = w_end

        # Strategy 3: Global proportional distribution fallback if needed
        if not subtitle_words:
            all_words = text.strip().split()
            dur_per_word = total_duration / max(1, len(all_words))
            for i, w in enumerate(all_words):
                w_start = i * dur_per_word
                w_end = min(total_duration, (i + 1) * dur_per_word)
                subtitle_words.append(SubtitleWord(
                    word=w,
                    start=round(w_start, 3),
                    end=round(w_end, 3),
                    is_emphasized=self._check_emphasis(w)
                ))

        return total_duration, subtitle_words

    def _check_emphasis(self, word: str) -> bool:
        clean = word.lower().strip(".,!?:;$\"'")
        return clean in EMPHASIS_KEYWORDS or any(c.isdigit() for c in word)

    def synthesize_sync(self, text: str, output_path: Path) -> Tuple[float, List[SubtitleWord]]:
        return asyncio.run(self.synthesize(text, output_path))
