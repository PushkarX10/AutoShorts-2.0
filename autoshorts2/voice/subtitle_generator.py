"""Subtitle Export Engine (.srt and .ass) for AutoShorts 2.0
Produces burned-in styled subtitle tracks with electric neon pink highlights.
"""

from pathlib import Path
from typing import List
from autoshorts2.models import SubtitleWord

def format_timestamp_srt(seconds: float) -> str:
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

def format_timestamp_ass(seconds: float) -> str:
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    centis = int(round((seconds - int(seconds)) * 100))
    return f"{hrs:01d}:{mins:02d}:{secs:02d}.{centis:02d}"

class SubtitleGenerator:
    def export_srt(self, words: List[SubtitleWord], output_path: Path, chunk_size: int = 4) -> Path:
        """Groups words into short, high-retention 3-5 word bursts."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        lines = []
        cue_idx = 1
        
        for i in range(0, len(words), chunk_size):
            chunk = words[i:i + chunk_size]
            start_t = chunk[0].start
            end_t = chunk[-1].end
            
            # Text line
            text_parts = []
            for w in chunk:
                if w.is_emphasized:
                    text_parts.append(f"<font color=\"#FF2A85\"><b>{w.word}</b></font>")
                else:
                    text_parts.append(w.word)
            text_line = " ".join(text_parts)
            
            lines.append(f"{cue_idx}")
            lines.append(f"{format_timestamp_srt(start_t)} --> {format_timestamp_srt(end_t)}")
            lines.append(text_line)
            lines.append("")
            cue_idx += 1
            
        output_path.write_text("\n".join(lines), encoding="utf-8")
        return output_path

    def export_ass(self, words: List[SubtitleWord], output_path: Path, chunk_size: int = 4) -> Path:
        """Exports high-fidelity ASS subtitle format with custom font styling."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        header = """[Script Info]
Title: AutoShorts 2.0 Cinematic Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Outfit,64,&H00FFFFFF,&H00852AFF,&H00121111,&H80000000,-1,0,0,0,100,100,0,0,1,5,10,2,60,60,320,1
Style: PinkEmphasis,Outfit,70,&H00852AFF,&H00FFFFFF,&H00121111,&H80000000,-1,0,0,0,105,105,0,0,1,6,12,2,60,60,320,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        events = []
        for i in range(0, len(words), chunk_size):
            chunk = words[i:i + chunk_size]
            start_str = format_timestamp_ass(chunk[0].start)
            end_str = format_timestamp_ass(chunk[-1].end)
            
            parts = []
            for w in chunk:
                if w.is_emphasized:
                    # In ASS, {\c&H852AFF&} is hot pink BGR
                    parts.append(r"{\c&H852AFF&}" + w.word.upper() + r"{\c&HFFFFFF&}")
                else:
                    parts.append(w.word.upper())
            line_text = " ".join(parts)
            events.append(f"Dialogue: 0,{start_str},{end_str},Default,,0,0,0,,{line_text}")
            
        full_content = header + "\n".join(events) + "\n"
        output_path.write_text(full_content, encoding="utf-8")
        return output_path
