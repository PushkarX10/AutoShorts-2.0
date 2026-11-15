import React from "react";
import { useCurrentFrame } from "remotion";

interface EnvironmentProps {
  environment: string;
  lighting: string;
}

export const CinematicEnvironment: React.FC<EnvironmentProps> = ({
  environment,
  lighting,
}) => {
  const frame = useCurrentFrame();

  // Subtle ambient particle floating (dust motes / gold glints)
  const particles = [
    { x: 220, y: 400, r: 3, speed: 0.8 },
    { x: 740, y: 620, r: 2.5, speed: 1.1 },
    { x: 380, y: 920, r: 3.5, speed: 0.6 },
    { x: 880, y: 1240, r: 2, speed: 0.9 },
    { x: 160, y: 1520, r: 3, speed: 0.7 },
  ];

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        backgroundColor: "#0D0E12",
        overflow: "hidden",
      }}
    >
      <svg
        viewBox="0 0 1080 1920"
        style={{ width: "100%", height: "100%" }}
        preserveAspectRatio="xMidYMid slice"
      >
        <defs>
          {/* Gritty Noise Grain */}
          <radialGradient id="lamp-glow" cx="50%" cy="30%" r="65%">
            <stop offset="0%" stopColor="#FFAE52" stopOpacity="0.35" />
            <stop offset="60%" stopColor="#FFAE52" stopOpacity="0.08" />
            <stop offset="100%" stopColor="#0D0E12" stopOpacity="0.95" />
          </radialGradient>
          <radialGradient id="pink-ambient" cx="80%" cy="20%" r="70%">
            <stop offset="0%" stopColor="#FF2A85" stopOpacity="0.25" />
            <stop offset="65%" stopColor="#FF2A85" stopOpacity="0.04" />
            <stop offset="100%" stopColor="#0D0E12" stopOpacity="0.95" />
          </radialGradient>
          <radialGradient id="blue-street" cx="50%" cy="80%" r="70%">
            <stop offset="0%" stopColor="#1E293B" stopOpacity="0.6" />
            <stop offset="100%" stopColor="#0B0D13" stopOpacity="0.98" />
          </radialGradient>
        </defs>

        {/* --- BACKGROUND LAYER --- */}
        {environment === "dim_apartment_desk" ? (
          <>
            {/* Dim Room Walls */}
            <rect x="0" y="0" width="1080" height="1920" fill="#14151C" />
            {/* Window with Venetian Blinds in Background */}
            <g opacity="0.6">
              <rect x="180" y="240" width="720" height="780" fill="#0A0C14" rx="8" />
              {/* Rain Streaks on Window */}
              {[...Array(16)].map((_, i) => (
                <line
                  key={i}
                  x1={220 + i * 44}
                  y1={240 + ((frame * 6 + i * 37) % 780)}
                  x2={210 + i * 44}
                  y2={270 + ((frame * 6 + i * 37) % 780)}
                  stroke="#38BDF8"
                  strokeWidth="2"
                  opacity="0.35"
                />
              ))}
              {/* Blinds horizontal lines */}
              {[...Array(24)].map((_, i) => (
                <line
                  key={`blind-${i}`}
                  x1="180"
                  y1={250 + i * 32}
                  x2="900"
                  y2={250 + i * 32}
                  stroke="#181A24"
                  strokeWidth="8"
                />
              ))}
            </g>
            {/* Ambient Lighting Overlay */}
            <rect x="0" y="0" width="1080" height="1920" fill="url(#lamp-glow)" />
            <rect x="0" y="0" width="1080" height="1920" fill="url(#pink-ambient)" />

            {/* Heavy Wooden Desk (Midground) */}
            <polygon points="0,1280 1080,1280 1080,1920 0,1920" fill="#1C1817" />
            <line x1="0" y1="1280" x2="1080" y2="1280" stroke="#382E2B" strokeWidth="8" />

            {/* Glowing Laptop Screen on Desk */}
            <g transform="translate(420, 1140)">
              {/* Laptop screen */}
              <polygon points="0,0 240,-30 240,110 0,140" fill="#0A0A10" stroke="#475569" strokeWidth="5" />
              <polygon points="12,10 228,-18 228,95 12,122" fill="#0F172A" />
              {/* Website interface lines & pink buy button */}
              <rect x="30" y="25" width="120" height="12" fill="#38BDF8" rx="3" />
              <rect x="30" y="50" width="160" height="8" fill="#64748B" rx="2" />
              <rect x="30" y="68" width="90" height="8" fill="#64748B" rx="2" />
              <rect x="30" y="90" width="80" height="18" fill="#FF2A85" rx="4" />
              {/* Screen Glow */}
              <circle cx="120" cy="50" r="140" fill="#38BDF8" opacity="0.12" />
            </g>
          </>
        ) : environment === "street_curbside" || environment === "street_night" ? (
          <>
            {/* Night City Skyline */}
            <rect x="0" y="0" width="1080" height="1920" fill="#0B0D13" />
            {/* Distant building silhouettes with glowing square windows */}
            <rect x="60" y="400" width="280" height="1100" fill="#12151E" />
            <rect x="380" y="280" width="340" height="1220" fill="#171A26" />
            <rect x="760" y="460" width="260" height="1040" fill="#10131B" />
            {/* Neon Pink Rooftop Sign */}
            <g transform="translate(430, 320)">
              <rect x="0" y="0" width="240" height="50" fill="#101118" stroke="#FF2A85" strokeWidth="4" rx="6" />
              <text x="120" y="34" textAnchor="middle" fill="#FF2A85" fontSize="22" fontWeight="900" fontFamily="sans-serif">US MINT</text>
            </g>
            {/* Wet Asphalt Street (Bottom Half) */}
            <polygon points="0,1320 1080,1320 1080,1920 0,1920" fill="#111319" />
            {/* Yellow street dashed line with wet specular reflection */}
            {[...Array(6)].map((_, i) => (
              <rect key={i} x={520} y={1350 + i * 110} width="35" height="65" fill="#EAB308" opacity="0.6" rx="4" />
            ))}
            {/* Armored Truck Silhouette */}
            <g transform="translate(180, 1080)">
              <rect x="0" y="0" width="700" height="340" fill="#1E2330" stroke="#0F121A" strokeWidth="8" rx="16" />
              <rect x="520" y="60" width="160" height="110" fill="#38BDF8" opacity="0.4" rx="8" />
              {/* Giant Armored Wheels */}
              <circle cx="160" cy="340" r="75" fill="#101116" stroke="#475569" strokeWidth="12" />
              <circle cx="560" cy="340" r="75" fill="#101116" stroke="#475569" strokeWidth="12" />
              {/* Headlights piercing cone */}
              <polygon points="680,180 1080,120 1080,380 680,240" fill="#FEF08A" opacity="0.18" />
            </g>
          </>
        ) : environment === "apartment_boxes" || environment === "dim_apartment_hallway" ? (
          <>
            {/* Apartment Room Packed With Giant Stacks of Boxes */}
            <rect x="0" y="0" width="1080" height="1920" fill="#13141C" />
            <rect x="0" y="0" width="1080" height="1920" fill="url(#lamp-glow)" />
            <rect x="0" y="0" width="1080" height="1920" fill="url(#pink-ambient)" />

            {/* Wooden Floorboards */}
            <polygon points="0,1360 1080,1360 1080,1920 0,1920" fill="#1B1716" />
            {[...Array(8)].map((_, i) => (
              <line key={i} x1={i * 155} y1="1360" x2={i * 190 - 100} y2="1920" stroke="#2B2422" strokeWidth="5" />
            ))}

            {/* Towering Stacks of Cardboard Boxes Stamped 'US MINT $250' */}
            {/* Left Box Tower */}
            <g transform="translate(40, 780)">
              {[...Array(4)].map((_, i) => (
                <g key={i} transform={`translate(${i * 12}, ${i * 140})`}>
                  <rect x="0" y="0" width="290" height="130" fill="#8B6946" stroke="#3D2B1A" strokeWidth="6" rx="4" />
                  <line x1="0" y1="65" x2="290" y2="65" stroke="#D97706" strokeWidth="8" opacity="0.6" />
                  <rect x="40" y="25" width="140" height="40" fill="#FFFFFF" rx="2" opacity="0.9" />
                  <text x="110" y="52" textAnchor="middle" fill="#111116" fontSize="18" fontWeight="900" fontFamily="sans-serif">US MINT $250</text>
                </g>
              ))}
            </g>

            {/* Right Box Tower */}
            <g transform="translate(740, 720)">
              {[...Array(5)].map((_, i) => (
                <g key={i} transform={`translate(${-i * 10}, ${i * 135})`}>
                  <rect x="0" y="0" width="280" height="125" fill="#96724E" stroke="#3D2B1A" strokeWidth="6" rx="4" />
                  <line x1="0" y1="62" x2="280" y2="62" stroke="#D97706" strokeWidth="8" opacity="0.6" />
                  <rect x="40" y="22" width="130" height="38" fill="#FFFFFF" rx="2" opacity="0.9" />
                  <text x="105" y="48" textAnchor="middle" fill="#111116" fontSize="16" fontWeight="900" fontFamily="sans-serif">$1 COINS</text>
                </g>
              ))}
            </g>
          </>
        ) : (
          /* Bank Lobby & Vault Architecture */
          <>
            <rect x="0" y="0" width="1080" height="1920" fill="#151720" />
            {/* Polished Marble Floor */}
            <polygon points="0,1300 1080,1300 1080,1920 0,1920" fill="#0F1118" />
            <line x1="0" y1="1300" x2="1080" y2="1300" stroke="#334155" strokeWidth="6" />

            {/* Massive Circular Steel Vault Door in Background */}
            <g transform="translate(540, 850)">
              <circle cx="0" cy="0" r="380" fill="#1E2330" stroke="#475569" strokeWidth="24" />
              <circle cx="0" cy="0" r="320" fill="#0F121A" stroke="#334155" strokeWidth="12" />
              {/* Steel Locking Bolts */}
              {[...Array(12)].map((_, i) => {
                const angle = (i * 30 * Math.PI) / 180;
                const bx = Math.cos(angle) * 350;
                const by = Math.sin(angle) * 350;
                return <circle key={i} cx={bx} cy={by} r="18" fill="#94A3B8" stroke="#1E2330" strokeWidth="6" />;
              })}
              {/* Vault Center Wheel */}
              <circle cx="0" cy="0" r="90" fill="#475569" stroke="#1E293B" strokeWidth="14" />
            </g>

            {/* Bank Teller Counter Desk (Foreground Midground) */}
            <polygon points="0,1380 1080,1380 1080,1920 0,1920" fill="#1A1D27" />
            <rect x="120" y="1260" width="840" height="120" fill="#242836" stroke="#475569" strokeWidth="6" rx="10" />
            {/* Frosted Glass Teller Dividers */}
            <rect x="180" y="980" width="220" height="280" fill="#94A3B8" opacity="0.2" rx="8" stroke="#64748B" strokeWidth="4" />
            <rect x="680" y="980" width="220" height="280" fill="#94A3B8" opacity="0.2" rx="8" stroke="#64748B" strokeWidth="4" />
          </>
        )}

        {/* --- FLOATING PARTICLES / GOLDEN COIN DUST --- */}
        {particles.map((p, i) => {
          const cy = (p.y - frame * p.speed * 2) % 1920;
          return (
            <circle
              key={i}
              cx={p.x + Math.sin(frame * 0.05 + i) * 15}
              cy={cy < 0 ? cy + 1920 : cy}
              r={p.r}
              fill="#F59E0B"
              opacity="0.45"
            />
          );
        })}
      </svg>
    </div>
  );
};
