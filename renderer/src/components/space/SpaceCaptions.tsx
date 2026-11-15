import React from "react";
import { useCurrentFrame } from "remotion";
import { SubtitleWordData } from "../../types/schema";

interface SpaceCaptionsProps {
  words: SubtitleWordData[];
}

export const SpaceCaptions: React.FC<SpaceCaptionsProps> = ({ words }) => {
  const frame = useCurrentFrame();
  const currentTime = frame / 30.0;

  if (!words || words.length === 0) return null;

  // Find active word index
  let activeIndex = -1;
  for (let i = 0; i < words.length; i++) {
    if (currentTime >= words[i].start && currentTime <= words[i].end + 0.12) {
      activeIndex = i;
      break;
    }
  }

  // Grace fallback for speaking pauses
  if (activeIndex === -1) {
    for (let i = words.length - 1; i >= 0; i--) {
      if (currentTime >= words[i].start && currentTime <= words[i].end + 0.35) {
        activeIndex = i;
        break;
      }
    }
  }

  if (activeIndex === -1) return null;

  // High-retention short 3-word window
  const windowSize = 3;
  const chunkStart = Math.max(0, activeIndex - (activeIndex % windowSize));
  const chunkEnd = Math.min(words.length, chunkStart + windowSize);
  const currentChunk = words.slice(chunkStart, chunkEnd);

  const ELECTRIC_CYAN = "#55D7E8";
  const SOLAR_YELLOW = "#FFD36B";
  const MARS_RED = "#C65B45";
  const WHITE = "#F5F6F8";

  return (
    <div
      style={{
        position: "absolute",
        bottom: 110,
        left: 0,
        width: "100%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 80,
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          display: "flex",
          gap: 16,
          alignItems: "center",
          justifyContent: "center",
          background: "rgba(8, 11, 20, 0.88)",
          backdropFilter: "blur(14px)",
          border: "2px solid #536780",
          borderRadius: 20,
          padding: "16px 36px",
          boxShadow: "0 10px 30px rgba(0, 0, 0, 0.8)",
          maxWidth: "88%",
        }}
      >
        {currentChunk.map((w, idx) => {
          const globalIdx = chunkStart + idx;
          const isCurrentWord = globalIdx === activeIndex;

          const wordColor = isCurrentWord
            ? w.is_emphasized ? SOLAR_YELLOW : ELECTRIC_CYAN
            : w.is_emphasized ? SOLAR_YELLOW : WHITE;

          return (
            <span
              key={`${globalIdx}-${w.word}`}
              style={{
                fontSize: isCurrentWord ? 42 : 36,
                fontWeight: 900,
                color: wordColor,
                textTransform: "uppercase",
                letterSpacing: "2px",
                transform: isCurrentWord ? "scale(1.12)" : "scale(1.0)",
                transition: "transform 0.1s ease-out, color 0.1s ease-out",
                textShadow: isCurrentWord
                  ? `0 0 18px ${w.is_emphasized ? "#FFD36B" : "#55D7E8"}`
                  : "0 2px 6px rgba(0,0,0,0.8)",
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
