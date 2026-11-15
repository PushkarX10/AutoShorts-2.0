import React from "react";
import { useCurrentFrame } from "remotion";

export interface SpaceHUDState {
  planet: string;
  solDay: string;
  oxygenPercent: number;
  temperature: string;
  gravity: string;
  pressure: string;
  alertLevel?: "normal" | "warning" | "critical";
}

interface SpaceHUDProps {
  state: SpaceHUDState;
}

/**
 * Editorial Mission Field-Log Header Plate (v2.0)
 * Replaces generic glowing sci-fi HUD with an authentic scientific journal field-log header:
 * - Ink Charcoal (#242B35) & Paper Cream (#F4EFE5) with Stone Grey & Warm Gold accents
 * - Tactile analog dial indicator for Oxygen Reserve
 * - Clean typographic telemetry stamp: "EXPEDITION FIELD LOG // SOL 18"
 * - Anchored safely at top: 70px
 */
export const SpaceHUD: React.FC<SpaceHUDProps> = ({ state }) => {
  const frame = useCurrentFrame();

  const {
    planet = "Mars",
    solDay = "SOL 18",
    oxygenPercent = 88,
    temperature = "-63°C",
    gravity = "0.38g",
    alertLevel = "normal",
  } = state;

  const isCritical = alertLevel === "critical" || oxygenPercent < 30;

  // Palette from v2.0
  const PAPER_CREAM = "#F4EFE5";
  const INK_CHARCOAL = "#242B35";
  const DUSTY_CORAL = "#C86D52";
  const WARM_GOLD = "#D5AA62";
  const STONE_GREY = "#A6A18F";
  const SAGE_GREEN = "#768C79";
  const MUTED_BLUE = "#527A9B";

  // Alert pulse for critical crisis (Scene 5 & 6)
  const alertPulse = isCritical && frame % 16 < 8;

  // Oxygen dial needle angle (-90deg to +90deg based on 0-100%)
  const needleAngle = -90 + (oxygenPercent / 100) * 180;

  return (
    <div
      style={{
        position: "absolute",
        top: 70,
        left: 0,
        width: "100%",
        display: "flex",
        justifyContent: "center",
        zIndex: 85,
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          width: 960,
          background: isCritical && alertPulse ? DUSTY_CORAL : INK_CHARCOAL,
          border: `3px solid ${isCritical ? DUSTY_CORAL : STONE_GREY}`,
          borderRadius: 16,
          padding: "16px 28px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          boxShadow: "0 10px 25px rgba(36, 43, 53, 0.45)",
          transition: "background 0.2s ease",
        }}
      >
        {/* --- LEFT: EXPEDITION LOG STAMP & PLANETARY SEAL --- */}
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <svg width="46" height="46" viewBox="0 0 46 46">
            {/* Outer Compass / Seal Ring */}
            <circle cx="23" cy="23" r="21" fill="none" stroke={WARM_GOLD} strokeWidth="2.5" />
            <circle cx="23" cy="23" r="17" fill="none" stroke={STONE_GREY} strokeWidth="1" strokeDasharray="3 3" />
            {/* Center Planet Icon */}
            <circle cx="23" cy="23" r="9" fill={DUSTY_CORAL} stroke={PAPER_CREAM} strokeWidth="2" />
            {/* Cardinal ticks */}
            <line x1="23" y1="2" x2="23" y2="7" stroke={WARM_GOLD} strokeWidth="2" />
            <line x1="23" y1="39" x2="23" y2="44" stroke={WARM_GOLD} strokeWidth="2" />
            <line x1="2" y1="23" x2="7" y2="23" stroke={WARM_GOLD} strokeWidth="2" />
            <line x1="39" y1="23" x2="44" y2="23" stroke={WARM_GOLD} strokeWidth="2" />
          </svg>

          <div>
            <div
              style={{
                fontSize: 13,
                fontWeight: 900,
                letterSpacing: 3,
                color: WARM_GOLD,
                textTransform: "uppercase",
                fontFamily: "monospace",
              }}
            >
              EXPEDITION FIELD LOG
            </div>
            <div
              style={{
                fontSize: 26,
                fontWeight: 900,
                color: PAPER_CREAM,
                letterSpacing: 1.5,
                fontFamily: "'Outfit', sans-serif",
              }}
            >
              {planet.toUpperCase()} // <span style={{ color: WARM_GOLD }}>{solDay}</span>
            </div>
          </div>
        </div>

        {/* --- CENTER: ANALOG OXYGEN GAUGE DIAL --- */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 14,
            background: "rgba(244, 239, 229, 0.08)",
            padding: "8px 20px",
            borderRadius: 12,
            border: "1px solid rgba(166, 161, 143, 0.3)",
          }}
        >
          {/* Dial SVG */}
          <svg width="44" height="44" viewBox="0 0 44 44">
            {/* Dial Arc */}
            <circle cx="22" cy="22" r="18" fill="#1C222A" stroke={STONE_GREY} strokeWidth="2.5" />
            {/* Color Zone: Red for low O2, Sage Green for safe */}
            <path
              d="M 10 30 A 15 15 0 0 1 34 30"
              fill="none"
              stroke={isCritical ? DUSTY_CORAL : SAGE_GREEN}
              strokeWidth="3.5"
            />
            {/* Dial Pivot */}
            <circle cx="22" cy="22" r="3" fill={PAPER_CREAM} />
            {/* Needle */}
            <line
              x1="22"
              y1="22"
              x2="22"
              y2="8"
              stroke={isCritical ? DUSTY_CORAL : WARM_GOLD}
              strokeWidth="2.5"
              strokeLinecap="round"
              transform={`rotate(${needleAngle}, 22, 22)`}
            />
          </svg>

          <div>
            <div
              style={{
                fontSize: 12,
                fontWeight: 800,
                color: STONE_GREY,
                letterSpacing: 2,
                fontFamily: "monospace",
              }}
            >
              OXYGEN RESERVE
            </div>
            <div
              style={{
                fontSize: 22,
                fontWeight: 900,
                color: isCritical ? DUSTY_CORAL : SAGE_GREEN,
                fontFamily: "monospace",
              }}
            >
              {oxygenPercent}% {isCritical ? "CRITICAL" : "NOMINAL"}
            </div>
          </div>
        </div>

        {/* --- RIGHT: PHYSICAL CONSTANTS (TEMP & GRAVITY) --- */}
        <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
          <div>
            <div
              style={{
                fontSize: 12,
                fontWeight: 800,
                color: STONE_GREY,
                letterSpacing: 1.5,
                fontFamily: "monospace",
              }}
            >
              TEMP
            </div>
            <div
              style={{
                fontSize: 20,
                fontWeight: 900,
                color: MUTED_BLUE,
                fontFamily: "monospace",
              }}
            >
              {temperature}
            </div>
          </div>

          <div
            style={{
              width: 1,
              height: 36,
              background: STONE_GREY,
              opacity: 0.4,
            }}
          />

          <div>
            <div
              style={{
                fontSize: 12,
                fontWeight: 800,
                color: STONE_GREY,
                letterSpacing: 1.5,
                fontFamily: "monospace",
              }}
            >
              GRAVITY
            </div>
            <div
              style={{
                fontSize: 20,
                fontWeight: 900,
                color: WARM_GOLD,
                fontFamily: "monospace",
              }}
            >
              {gravity}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
