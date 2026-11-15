import React from "react";
import { interpolate, useCurrentFrame, spring } from "remotion";
import { InfographicSpecData } from "../types/schema";

interface InfographicProps {
  spec?: InfographicSpecData;
  durationInFrames: number;
}

export const InfographicDocumentary: React.FC<InfographicProps> = ({
  spec,
  durationInFrames,
}) => {
  const frame = useCurrentFrame();

  if (!spec) return null;

  // Staggered reveal of infographic elements using Remotion springs
  const headerSpring = spring({
    frame,
    fps: 30,
    config: { damping: 14, stiffness: 120 },
  });

  const cardsSpring = spring({
    frame: frame - 6,
    fps: 30,
    config: { damping: 14, stiffness: 120 },
  });

  const thresholdSpring = spring({
    frame: frame - 16,
    fps: 30,
    config: { damping: 12, stiffness: 100 },
  });

  const pulse = Math.sin(frame * 0.15) * 4;

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        backgroundColor: "#F4EFEB",
        color: "#111114",
        padding: "290px 70px 140px 70px",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        boxSizing: "border-box",
        zIndex: 40,
        fontFamily: "'Outfit', 'Montserrat', -apple-system, sans-serif",
      }}
    >
      {/* Subtle paper grain / micro texture pattern */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          opacity: 0.04,
          backgroundImage:
            "radial-gradient(#111114 1px, transparent 1px), radial-gradient(#111114 1px, #F4EFEB 1px)",
          backgroundSize: "20px 20px",
          backgroundPosition: "0 0, 10px 10px",
          pointerEvents: "none",
        }}
      />

      {/* --- HEADER TITLE & SUBTITLE --- */}
      <div
        style={{
          transform: `translateY(${interpolate(headerSpring, [0, 1], [40, 0])}px)`,
          opacity: headerSpring,
          display: "flex",
          flexDirection: "column",
          gap: 12,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
          <div style={{ width: 14, height: 14, backgroundColor: "#FF2A85", borderRadius: 3 }} />
          <span
            style={{
              fontSize: 22,
              fontWeight: 800,
              letterSpacing: "0.18em",
              color: "#64748B",
              textTransform: "uppercase",
            }}
          >
            {spec.subtitle}
          </span>
        </div>

        <h1
          style={{
            fontSize: 66,
            fontWeight: 900,
            lineHeight: 1.05,
            letterSpacing: "-0.04em",
            color: "#111114",
            margin: 0,
            textTransform: "uppercase",
          }}
        >
          {spec.title}
        </h1>

        <div style={{ width: 140, height: 7, backgroundColor: "#FF2A85", borderRadius: 4 }} />
      </div>

      {/* --- CORE BREAKDOWN GRID (4 CARDS) --- */}
      <div
        style={{
          transform: `translateY(${interpolate(cardsSpring, [0, 1], [50, 0])}px)`,
          opacity: cardsSpring,
          display: "flex",
          flexDirection: "column",
          gap: 20,
          margin: "30px 0",
        }}
      >
        {spec.breakdown_items.map((item, idx) => (
          <div
            key={idx}
            style={{
              backgroundColor: "#EAE3DA",
              borderRadius: 18,
              padding: "24px 32px",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              border: "2px solid #D5CCC1",
              boxShadow: "0 8px 24px rgba(0,0,0,0.04)",
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
              <span
                style={{
                  fontSize: 24,
                  fontWeight: 900,
                  color: "#94A3B8",
                  fontFamily: "monospace",
                }}
              >
                0{idx + 1}
              </span>
              <span
                style={{
                  fontSize: 28,
                  fontWeight: 800,
                  color: "#1E293B",
                  letterSpacing: "-0.01em",
                }}
              >
                {item.label}
              </span>
            </div>

            <span
              style={{
                fontSize: 34,
                fontWeight: 900,
                color: item.val.includes("+") ? "#FF2A85" : "#111114",
                fontFamily: "monospace",
              }}
            >
              {item.val}
            </span>
          </div>
        ))}
      </div>

      {/* --- VISUAL THRESHOLD / SPREAD HIGHLIGHT BOX --- */}
      <div
        style={{
          transform: `scale(${interpolate(thresholdSpring, [0, 1], [0.92, 1])})`,
          opacity: thresholdSpring,
          backgroundColor: "#111114",
          borderRadius: 22,
          padding: "36px 40px",
          color: "#FFFFFF",
          display: "flex",
          flexDirection: "column",
          gap: 16,
          boxShadow: "0 22px 50px rgba(17, 17, 20, 0.25)",
          border: "2px solid rgba(255, 42, 133, 0.4)",
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <span
            style={{
              fontSize: 20,
              fontWeight: 800,
              color: "#94A3B8",
              letterSpacing: "0.15em",
              textTransform: "uppercase",
            }}
          >
            {spec.threshold_label}
          </span>
          <span
            style={{
              fontSize: 48,
              fontWeight: 900,
              color: "#FF2A85",
              fontFamily: "monospace",
              textShadow: "0 0 20px rgba(255, 42, 133, 0.6)",
            }}
          >
            {spec.threshold_value}
          </span>
        </div>

        {/* Dynamic neon pink threshold line */}
        <div
          style={{
            width: "100%",
            height: 8,
            backgroundColor: "rgba(255, 255, 255, 0.15)",
            borderRadius: 4,
            overflow: "hidden",
          }}
        >
          <div
            style={{
              width: "100%",
              height: "100%",
              background: "linear-gradient(90deg, #FF2A85 0%, #FF60A8 100%)",
              boxShadow: "0 0 16px #FF2A85",
            }}
          />
        </div>

        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <span style={{ fontSize: 20, fontWeight: 700, color: "#E2E8F0" }}>
            RESULTING ARBITRAGE:
          </span>
          <span
            style={{
              fontSize: 24,
              fontWeight: 900,
              color: "#34D399",
              letterSpacing: "0.08em",
            }}
          >
            {spec.pink_highlight_stat}
          </span>
        </div>
      </div>
    </div>
  );
};
