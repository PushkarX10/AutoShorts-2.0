import React from "react";
import { useCurrentFrame } from "remotion";

export interface SpaceHudState {
  planet: string;
  solDay: string;
  oxygenPercent: number;
  temperature: string;
  gravity: string;
  pressure: string;
  alertLevel?: "normal" | "warning" | "critical";
}

interface SpaceHUDProps {
  state?: SpaceHudState;
}

export const SpaceHUD: React.FC<SpaceHUDProps> = ({ state }) => {
  const frame = useCurrentFrame();

  if (!state) return null;

  const SPACE_BLACK = "#080B14";
  const DEEP_SPACE_NAVY = "#10182A";
  const MIDNIGHT_BLUE = "#182744";
  const STEEL_BLUE = "#536780";
  const PLANETARY_ORANGE = "#F18B45";
  const MARS_RED = "#C65B45";
  const ELECTRIC_CYAN = "#55D7E8";
  const SOLAR_YELLOW = "#FFD36B";
  const OXYGEN_GREEN = "#7BD69A";
  const WHITE = "#F5F6F8";

  const isAlert = state.alertLevel === "critical" || state.oxygenPercent < 30;
  const pulse = Math.sin(frame * 0.3) * 0.5 + 0.5;

  // Oxygen meter animated sweep
  const o2Color =
    state.oxygenPercent > 50 ? OXYGEN_GREEN :
    state.oxygenPercent > 25 ? SOLAR_YELLOW : MARS_RED;

  // Radar sweep angle
  const radarAngle = (frame * 6) % 360;

  return (
    <div
      style={{
        position: "absolute",
        top: 70,
        left: 0,
        width: "100%",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        zIndex: 50,
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          width: 960,
          background: "rgba(16, 24, 42, 0.92)",
          backdropFilter: "blur(18px)",
          border: `3px solid ${isAlert ? MARS_RED : STEEL_BLUE}`,
          borderRadius: 24,
          padding: "16px 24px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          boxShadow: isAlert
            ? `0 0 ${20 + pulse * 14}px rgba(198, 91, 69, 0.75)`
            : "0 12px 36px rgba(8, 11, 20, 0.65)",
        }}
      >
        {/* Left: Mission & Planet Identity */}
        <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
          {/* Rotating Planetary Sensor Radar */}
          <div
            style={{
              width: 52,
              height: 52,
              borderRadius: "50%",
              backgroundColor: SPACE_BLACK,
              border: `2px solid ${ELECTRIC_CYAN}`,
              position: "relative",
              overflow: "hidden",
            }}
          >
            <div
              style={{
                position: "absolute",
                top: "50%",
                left: "50%",
                width: 26,
                height: 2,
                backgroundColor: ELECTRIC_CYAN,
                transformOrigin: "0 0",
                transform: `rotate(${radarAngle}deg)`,
                boxShadow: `0 0 6px ${ELECTRIC_CYAN}`,
              }}
            />
            {/* Blips */}
            <div style={{ position: "absolute", top: 14, left: 28, width: 4, height: 4, borderRadius: "50%", backgroundColor: SOLAR_YELLOW }} />
            <div style={{ position: "absolute", top: 32, left: 16, width: 4, height: 4, borderRadius: "50%", backgroundColor: o2Color }} />
          </div>

          <div>
            <div
              style={{
                fontSize: 13,
                fontWeight: 900,
                color: STEEL_BLUE,
                letterSpacing: "2.5px",
                fontFamily: "monospace",
              }}
            >
              MISSION CONTROL // {state.planet.toUpperCase()}
            </div>
            <div
              style={{
                fontSize: 22,
                fontWeight: 900,
                color: WHITE,
                letterSpacing: "1px",
              }}
            >
              {state.solDay}
            </div>
          </div>
        </div>

        {/* Center: Live Oxygen Life Support Meter */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            width: 280,
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              width: "100%",
              marginBottom: 6,
            }}
          >
            <span
              style={{
                fontSize: 13,
                fontWeight: 900,
                color: o2Color,
                fontFamily: "monospace",
                letterSpacing: "1.5px",
              }}
            >
              LIFE SUPPORT // O₂ LEVEL
            </span>
            <span
              style={{
                fontSize: 18,
                fontWeight: 900,
                color: o2Color,
                fontFamily: "monospace",
              }}
            >
              {state.oxygenPercent}%
            </span>
          </div>

          {/* Animated Oxygen Bar */}
          <div
            style={{
              width: "100%",
              height: 10,
              backgroundColor: SPACE_BLACK,
              borderRadius: 6,
              overflow: "hidden",
              border: `1.5px solid ${o2Color}`,
            }}
          >
            <div
              style={{
                width: `${state.oxygenPercent}%`,
                height: "100%",
                backgroundColor: o2Color,
                borderRadius: 4,
                boxShadow: `0 0 10px ${o2Color}`,
                transition: "width 0.4s ease-out",
              }}
            />
          </div>
        </div>

        {/* Right: Environmental Telemetry (Gravity & Temp) */}
        <div style={{ display: "flex", gap: 20 }}>
          <div style={{ textAlign: "right" }}>
            <div style={{ fontSize: 11, fontWeight: 900, color: STEEL_BLUE, fontFamily: "monospace" }}>GRAVITY</div>
            <div style={{ fontSize: 17, fontWeight: 900, color: ELECTRIC_CYAN, fontFamily: "sans-serif" }}>{state.gravity}</div>
          </div>
          <div style={{ textAlign: "right" }}>
            <div style={{ fontSize: 11, fontWeight: 900, color: STEEL_BLUE, fontFamily: "monospace" }}>TEMP</div>
            <div style={{ fontSize: 17, fontWeight: 900, color: isAlert ? MARS_RED : SOLAR_YELLOW, fontFamily: "sans-serif" }}>{state.temperature}</div>
          </div>
        </div>
      </div>
    </div>
  );
};
