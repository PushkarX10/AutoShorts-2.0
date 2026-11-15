import React from "react";
import { useCurrentFrame } from "remotion";
import { SubtitleWordData } from "../../types/schema";

interface SpaceCaptionsProps {
  words: SubtitleWordData[];
}

/**
 * Clean Black & White Kinetic Subtitles
 * - High-contrast black & white theme
 * - Elevated position (bottom: 280px) safe from YouTube Shorts bottom overlays
 * - Human-designed typography (clean modern sans-serif, zero AI-tech monospace)
 * - Auto-wrapping dynamic flex container: zero overflow, zero text overlap
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

  // Grace fallback for natural speech pauses
  if (activeIndex === -1) {
    for (let i = words.length - 1; i >= 0; i--) {
      if (currentTime >= words[i].start && currentTime <= words[i].end + 0.35) {
        activeIndex = i;
        break;
      }
    }
  }

  if (activeIndex === -1) return null;

  // Clean 2 to 3 word reading chunks
  const windowSize = 3;
  const chunkStart = Math.max(0, activeIndex - (activeIndex % windowSize));
  const chunkEnd = Math.min(words.length, chunkStart + windowSize);
  const currentChunk = words.slice(chunkStart, chunkEnd);

  return (
    <div
      style={{
        position: "absolute",
        bottom: 280,
        left: 0,
        width: "100%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 80,
        pointerEvents: "none",
        padding: "0 40px",
        boxSizing: "border-box",
      }}
    >
      <div
        style={{
          display: "inline-flex",
          flexWrap: "wrap",
          gap: "10px 14px",
          alignItems: "center",
          justifyContent: "center",
          backgroundColor: "rgba(10, 12, 16, 0.92)",
          border: "2px solid rgba(255, 255, 255, 0.28)",
          borderRadius: 22,
          padding: "16px 28px",
          boxShadow: "0 14px 36px rgba(0, 0, 0, 0.75)",
          maxWidth: "92%",
          boxSizing: "border-box",
        }}
      >
        {currentChunk.map((w, idx) => {
          const globalIdx = chunkStart + idx;
          const isCurrentWord = globalIdx === activeIndex;

          if (isCurrentWord) {
            return (
              <span
                key={`${globalIdx}-${w.word}`}
                style={{
                  display: "inline-block",
                  backgroundColor: "#FFFFFF",
                  color: "#000000",
                  padding: "4px 12px",
                  borderRadius: 10,
                  fontSize: 38,
                  fontWeight: 900,
                  letterSpacing: "0.5px",
                  fontFamily:
                    'Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
                  transform: "scale(1.05)",
                  boxShadow: "0 4px 14px rgba(255, 255, 255, 0.35)",
                  lineHeight: 1.25,
                  whiteSpace: "nowrap",
                }}
              >
                {w.word}
              </span>
            );
          }

          return (
            <span
              key={`${globalIdx}-${w.word}`}
              style={{
                display: "inline-block",
                color: "rgba(255, 255, 255, 0.85)",
                fontSize: 36,
                fontWeight: 700,
                letterSpacing: "0.5px",
                fontFamily:
                  'Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
                lineHeight: 1.25,
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
