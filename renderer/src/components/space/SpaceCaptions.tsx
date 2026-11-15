import React from "react";
import { useCurrentFrame } from "remotion";
import { SubtitleWordData } from "../../types/schema";

interface SpaceCaptionsProps {
  words: SubtitleWordData[];
}

/**
 * Editorial Kinetic Subtitles (v2.0)
 * - Styled like an editorial journal annotation plate
 * - Deep Ink Charcoal (#242B35) pill with Stone Grey border and Paper Cream (#F4EFE5) typography
 * - Keyword highlights in Warm Gold (#D5AA62) and Dusty Coral (#C86D52)
 * - Strictly anchored at bottom: 110px (y: 1670px - 1810px) with 390px+ vertical clearance
 */
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

  // High-retention 3-word window
  const windowSize = 3;
  const chunkStart = Math.max(0, activeIndex - (activeIndex % windowSize));
  const chunkEnd = Math.min(words.length, chunkStart + windowSize);
  const currentChunk = words.slice(chunkStart, chunkEnd);

  // Palette from v2.0
  const PAPER_CREAM = "#F4EFE5";
  const INK_CHARCOAL = "#242B35";
  const WARM_GOLD = "#D5AA62";
  const DUSTY_CORAL = "#C86D52";
  const STONE_GREY = "#A6A18F";

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
          background: "rgba(36, 43, 53, 0.94)",
          backdropFilter: "blur(12px)",
          border: `2.5px solid ${STONE_GREY}`,
          borderRadius: 20,
          padding: "16px 36px",
          boxShadow: "0 12px 32px rgba(0, 0, 0, 0.65)",
          maxWidth: "88%",
        }}
      >
        {currentChunk.map((w, idx) => {
          const globalIdx = chunkStart + idx;
          const isCurrentWord = globalIdx === activeIndex;

          const wordColor = isCurrentWord
            ? w.is_emphasized ? WARM_GOLD : PAPER_CREAM
            : w.is_emphasized ? WARM_GOLD : "#D0C6B5";

          return (
            <span
              key={`${globalIdx}-${w.word}`}
              style={{
                fontSize: isCurrentWord ? 42 : 36,
                fontWeight: 900,
                color: wordColor,
                textTransform: "uppercase",
                letterSpacing: "2px",
                transform: isCurrentWord ? "scale(1.10)" : "scale(1.0)",
                transition: "transform 0.1s ease-out, color 0.1s ease-out",
                textShadow: isCurrentWord
                  ? `0 0 14px ${w.is_emphasized ? WARM_GOLD : "rgba(244, 239, 229, 0.7)"}`
                  : "0 2px 4px rgba(0,0,0,0.8)",
                display: "inline-block",
                fontFamily: "'Outfit', 'Montserrat', sans-serif",
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
