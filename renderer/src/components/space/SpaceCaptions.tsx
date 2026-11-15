import React from "react";
import { useCurrentFrame } from "remotion";
import { SubtitleWordData } from "../../types/schema";

interface SpaceCaptionsProps {
  words: SubtitleWordData[];
}

/**
 * Premium White & Black Kinetic YouTube Shorts Captions
 * - Strict High-Contrast White & Black aesthetic (Pure White fill with Heavy Black Stroke)
 * - Zero bounding box clipping: No rigid container to overflow or cut off words
 * - 100% visible across any background (dark space, bright red dunes, white lander, storm)
 * - High-impact bold typography with active word scale pop
 * - Elevated position (bottom: 320px) completely clear of Shorts UI overlays
 */
export const SpaceCaptions: React.FC<SpaceCaptionsProps> = ({ words }) => {
  const frame = useCurrentFrame();
  const currentTime = frame / 30.0;

  if (!words || words.length === 0) return null;

  // Find active word index
  let activeIndex = -1;
  for (let i = 0; i < words.length; i++) {
    if (currentTime >= words[i].start && currentTime <= words[i].end + 0.1) {
      activeIndex = i;
      break;
    }
  }

  // Grace fallback for natural pauses
  if (activeIndex === -1) {
    for (let i = words.length - 1; i >= 0; i--) {
      if (currentTime >= words[i].start && currentTime <= words[i].end + 0.3) {
        activeIndex = i;
        break;
      }
    }
  }

  if (activeIndex === -1) return null;

  // High-retention 2-3 word window
  const windowSize = 3;
  const chunkStart = Math.max(0, activeIndex - (activeIndex % windowSize));
  const chunkEnd = Math.min(words.length, chunkStart + windowSize);
  const currentChunk = words.slice(chunkStart, chunkEnd);

  return (
    <div
      style={{
        position: "absolute",
        bottom: 320,
        left: 0,
        width: "100%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 85,
        pointerEvents: "none",
        padding: "0 30px",
        boxSizing: "border-box",
      }}
    >
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "14px 20px",
          alignItems: "center",
          justifyContent: "center",
          maxWidth: 960,
          textAlign: "center",
        }}
      >
        {currentChunk.map((w, idx) => {
          const globalIdx = chunkStart + idx;
          const isCurrentWord = globalIdx === activeIndex;

          return (
            <span
              key={`${globalIdx}-${w.word}`}
              style={{
                display: "inline-block",
                color: "#FFFFFF",
                fontSize: isCurrentWord ? 56 : 46,
                fontWeight: 900,
                textTransform: "uppercase",
                letterSpacing: "1px",
                fontFamily:
                  '"Montserrat", "Arial Black", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                WebkitTextStroke: isCurrentWord ? "9px #000000" : "7px #000000",
                paintOrder: "stroke fill",
                filter: "drop-shadow(0 6px 14px rgba(0, 0, 0, 0.95))",
                transform: isCurrentWord ? "scale(1.12)" : "scale(0.96)",
                opacity: isCurrentWord ? 1.0 : 0.78,
                transition: "all 0.08s ease-out",
                lineHeight: 1.2,
                whiteSpace: "nowrap",
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
