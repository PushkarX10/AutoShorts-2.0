import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { HudStateData } from "../types/schema";

interface HudProps {
  state?: HudStateData;
}

export const InWorldHUD: React.FC<HudProps> = ({ state }) => {
  const frame = useCurrentFrame();

  if (!state) return null;

  // Pulse animation for high suspicion or active changes
  const pulse = Math.sin(frame * 0.25) * 0.5 + 0.5;

  return (
    <div
      style={{
        position: "absolute",
        top: 180,
        left: "50%",
        transform: "translateX(-50%)",
        width: 860,
        backgroundColor: "rgba(11, 13, 20, 0.88)",
        backdropFilter: "blur(14px)",
        borderRadius: 20,
        border: "1.5px solid rgba(255, 42, 133, 0.45)",
        boxShadow: "0 18px 40px rgba(0, 0, 0, 0.65), 0 0 24px rgba(255, 42, 133, 0.22)",
        padding: "18px 28px",
        display: "flex",
        flexDirection: "column",
        gap: 12,
        zIndex: 50,
        fontFamily: "'Outfit', 'Montserrat', -apple-system, sans-serif",
      }}
    >
      {/* 3 Metric Columns */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        {/* Column 1 */}
        <div style={{ display: "flex", flexDirection: "column", gap: 3 }}>
          <span
            style={{
              fontSize: 14,
              fontWeight: 800,
              color: "#94A3B8",
              letterSpacing: "0.14em",
              textTransform: "uppercase",
            }}
          >
            {state.label_1}
          </span>
          <span
            style={{
              fontSize: 26,
              fontWeight: 900,
              color: "#FFFFFF",
              letterSpacing: "0.02em",
              fontFamily: "monospace",
            }}
          >
            {state.val_1}
          </span>
        </div>

        {/* Divider */}
        <div style={{ width: 1.5, height: 38, backgroundColor: "rgba(255, 255, 255, 0.12)" }} />

        {/* Column 2 */}
        <div style={{ display: "flex", flexDirection: "column", gap: 3, alignItems: "center" }}>
          <span
            style={{
              fontSize: 14,
              fontWeight: 800,
              color: "#94A3B8",
              letterSpacing: "0.14em",
              textTransform: "uppercase",
            }}
          >
            {state.label_2}
          </span>
          <span
            style={{
              fontSize: 26,
              fontWeight: 900,
              color: "#34D399",
              letterSpacing: "0.02em",
              fontFamily: "monospace",
            }}
          >
            {state.val_2}
          </span>
        </div>

        {/* Divider */}
        <div style={{ width: 1.5, height: 38, backgroundColor: "rgba(255, 255, 255, 0.12)" }} />

        {/* Column 3 (Suspicion / Alert with Neon Pink Emphasis) */}
        <div style={{ display: "flex", flexDirection: "column", gap: 3, alignItems: "flex-end" }}>
          <span
            style={{
              fontSize: 14,
              fontWeight: 800,
              color: "#FF2A85",
              letterSpacing: "0.14em",
              textTransform: "uppercase",
            }}
          >
            {state.label_3}
          </span>
          <span
            style={{
              fontSize: 26,
              fontWeight: 900,
              color: "#FF2A85",
              letterSpacing: "0.02em",
              fontFamily: "monospace",
              textShadow: `0 0 ${10 + pulse * 8}px rgba(255, 42, 133, 0.8)`,
            }}
          >
            {state.val_3}
          </span>
        </div>
      </div>

      {/* Dynamic Animated Progress Bar */}
      <div
        style={{
          width: "100%",
          height: 6,
          backgroundColor: "rgba(255, 255, 255, 0.08)",
          borderRadius: 4,
          overflow: "hidden",
          position: "relative",
        }}
      >
        <div
          style={{
            height: "100%",
            width: `${state.progress_percent}%`,
            background: "linear-gradient(90deg, #FF2A85 0%, #F43F5E 100%)",
            boxShadow: "0 0 12px #FF2A85",
            transition: "width 0.4s ease-out",
          }}
        />
      </div>
    </div>
  );
};
