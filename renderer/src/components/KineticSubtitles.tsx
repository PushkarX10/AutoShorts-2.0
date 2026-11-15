import React from "react";
import { useCurrentFrame } from "remotion";
import { SubtitleWordData } from "../types/schema";

interface SubtitlesProps {
  words: SubtitleWordData[];
}

export const KineticSubtitles: React.FC<SubtitlesProps> = ({ words }) => {
  const frame = useCurrentFrame();
  const currentTime = frame / 30.0;

  if (!words || words.length === 0) return null;

  // Find currently active word index
  let activeIndex = -1;
  for (let i = 0; i < words.length; i++) {
    if (currentTime >= words[i].start && currentTime <= words[i].end + 0.15) {
      activeIndex = i;
      break;
    }
  }

  // If no word strictly matches, pick the closest preceding word within 0.4s
  if (activeIndex === -1) {
    for (let i = words.length - 1; i >= 0; i--) {
      if (currentTime >= words[i].start && currentTime <= words[i].end + 0.5) {
        activeIndex = i;
        break;
      }
    }
  }

  if (activeIndex === -1) return null;

  // Window of 3 to 4 words around active word
  const windowSize = 3;
  const chunkStart = Math.max(0, activeIndex - (activeIndex % windowSize));
  const chunkEnd = Math.min(words.length, chunkStart + windowSize);
  const currentChunk = words.slice(chunkStart, chunkEnd);

  return (
    <div
      style={{
        position: "absolute",
        bottom: 240,
        left: 0,
        width: "100%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 70,
        pointerEvents: "none",
        padding: "0 50px",
        boxSizing: "border-box",
      }}
    >
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          alignItems: "center",
          gap: "12px 20px",
          backgroundColor: "rgba(10, 11, 16, 0.72)",
          backdropFilter: "blur(8px)",
          padding: "16px 32px",
          borderRadius: 24,
          border: "1px solid rgba(255, 255, 255, 0.12)",
          boxShadow: "0 14px 34px rgba(0,0,0,0.6)",
          fontFamily: "'Outfit', 'Montserrat', -apple-system, sans-serif",
        }}
      >
        {currentChunk.map((w, idx) => {
          const globalIdx = chunkStart + idx;
          const isCurrentlySpoken = globalIdx === activeIndex;
          const isEmphasized = w.is_emphasized;

          return (
            <span
              key={globalIdx}
              style={{
                fontSize: 56,
                fontWeight: 900,
                textTransform: "uppercase",
                letterSpacing: "-0.02em",
                color: isCurrentlySpoken
                  ? isEmphasized
                    ? "#FF2A85"
                    : "#FFFFFF"
                  : isEmphasized
                  ? "rgba(255, 42, 133, 0.85)"
                  : "rgba(255, 255, 255, 0.75)",
                transform: isCurrentlySpoken ? "scale(1.10)" : "scale(1.0)",
                transition: "all 0.08s ease-out",
                textShadow: isCurrentlySpoken
                  ? isEmphasized
                    ? "0 0 26px rgba(255, 42, 133, 0.95), 0 4px 14px rgba(0,0,0,0.9)"
                    : "0 4px 18px rgba(0,0,0,0.95), 0 0 16px rgba(255,255,255,0.4)"
                  : "0 4px 14px rgba(0,0,0,0.85)",
                display: "inline-block",
              }}
            >
              {w.word}
            </span>
          );
        })}
      </div>
    </div>
  );
};
