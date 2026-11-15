import React from "react";
import { useCurrentFrame } from "remotion";

interface CharacterProps {
  expression: string;
  pose: string;
  x?: number; // percentage (0.0 to 1.0)
  y?: number;
  scale?: number;
}

export const IllustratedCharacter: React.FC<CharacterProps> = ({
  expression = "scheming_smirk",
  pose = "holding_coin",
  x = 0.5,
  y = 0.55,
  scale = 1.05,
}) => {
  const frame = useCurrentFrame();

  // Subtle natural breathing cycle (every 60 frames = 2 sec)
  const breath = Math.sin(frame * 0.1) * 3;
  // Natural blink every 90 frames for 4 frames
  const isBlinking = frame % 90 < 4 && expression !== "wide_shock";
  // Head micro-tilt
  const headBob = Math.sin(frame * 0.08) * 1.5;

  return (
    <div
      style={{
        position: "absolute",
        left: `${x * 100}%`,
        top: `${y * 100}%`,
        transform: `translate(-50%, -50%) scale(${scale})`,
        width: 480,
        height: 720,
        pointerEvents: "none",
        zIndex: 25,
      }}
    >
      <svg
        viewBox="0 0 480 720"
        style={{ width: "100%", height: "100%", overflow: "visible" }}
      >
        <defs>
          {/* Subtle drop shadow for depth */}
          <filter id="char-shadow" x="-30%" y="-30%" width="160%" height="160%">
            <feDropShadow dx="0" dy="16" stdDeviation="18" floodColor="rgba(0,0,0,0.5)" />
          </filter>
          {/* Neon Pink Accent Glow */}
          <filter id="pink-glow" x="-40%" y="-40%" width="180%" height="180%">
            <feGaussianBlur stdDeviation="8" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* --- LEGS & SNEAKERS --- */}
        <g stroke="#111116" strokeWidth="18" strokeLinecap="round" strokeLinejoin="round">
          {pose === "wheeling_cart" ? (
            <>
              {/* Walking forward stance */}
              <path d="M 215 500 L 175 580 L 150 655" />
              <path d="M 265 500 L 290 580 L 325 655" />
            </>
          ) : pose === "typing" ? (
            <>
              {/* Seated / angled stance */}
              <path d="M 210 500 L 195 560 L 205 650" />
              <path d="M 270 500 L 285 560 L 275 650" />
            </>
          ) : (
            <>
              {/* Confident stance */}
              <path d="M 210 500 L 190 580 L 180 655" />
              <path d="M 270 500 L 290 580 L 300 655" />
            </>
          )}
        </g>

        {/* Shoes (Chunky white streetwear sneakers with pink accent sole) */}
        <g>
          {pose === "wheeling_cart" ? (
            <>
              <path d="M 125 655 L 170 655 L 165 635 L 140 635 Z" fill="#FFFFFF" stroke="#111116" strokeWidth="6" />
              <path d="M 125 655 L 170 655" stroke="#FF2A85" strokeWidth="5" />
              <path d="M 305 655 L 350 655 L 345 635 L 320 635 Z" fill="#FFFFFF" stroke="#111116" strokeWidth="6" />
              <path d="M 305 655 L 350 655" stroke="#FF2A85" strokeWidth="5" />
            </>
          ) : (
            <>
              <path d="M 155 655 L 200 655 L 195 635 L 170 635 Z" fill="#FFFFFF" stroke="#111116" strokeWidth="6" />
              <path d="M 155 655 L 200 655" stroke="#FF2A85" strokeWidth="5" />
              <path d="M 280 655 L 325 655 L 320 635 L 295 635 Z" fill="#FFFFFF" stroke="#111116" strokeWidth="6" />
              <path d="M 280 655 L 325 655" stroke="#FF2A85" strokeWidth="5" />
            </>
          )}
        </g>

        {/* --- TORSO & HOODIE (Charcoal Black #16171E with thick hand-drawn outline) --- */}
        <g transform={`translate(0, ${breath})`} filter="url(#char-shadow)">
          {/* Main hoodie body */}
          <path
            d="M 175 285 C 145 345 160 495 170 510 L 310 510 C 320 495 335 345 305 285 Z"
            fill="#16171E"
            stroke="#111114"
            strokeWidth="11"
            strokeLinejoin="round"
          />

          {/* Hoodie kangaroo front pocket */}
          <path
            d="M 195 405 L 285 405 L 300 488 L 180 488 Z"
            fill="#121319"
            stroke="#111114"
            strokeWidth="6"
          />

          {/* Hot-Pink Neon Drawstrings */}
          <path d="M 220 290 L 216 362" stroke="#FF2A85" strokeWidth="5" strokeLinecap="round" filter="url(#pink-glow)" />
          <circle cx="216" cy="365" r="4" fill="#FF2A85" />
          <path d="M 260 290 L 264 362" stroke="#FF2A85" strokeWidth="5" strokeLinecap="round" filter="url(#pink-glow)" />
          <circle cx="264" cy="365" r="4" fill="#FF2A85" />

          {/* --- ARMS & HANDS DEPENDING ON POSE --- */}
          {pose === "holding_coin" ? (
            <g stroke="#111116" strokeWidth="16" strokeLinecap="round" strokeLinejoin="round" fill="none">
              {/* Left hand tucked in pocket */}
              <path d="M 175 305 L 150 375 L 195 425" />
              {/* Right arm extended outward to the right holding coin */}
              <path d="M 305 305 L 375 260 L 380 185" />
              {/* Shiny Gold $1 Coin */}
              <g transform="translate(385, 175)">
                <circle cx="0" cy="0" r="30" fill="#F4BA3B" stroke="#B87D10" strokeWidth="6" filter="url(#char-shadow)" />
                <circle cx="0" cy="0" r="23" fill="#FFD05B" stroke="#B87D10" strokeWidth="2.5" />
                <text x="0" y="9" textAnchor="middle" fill="#7A4C05" fontSize="24" fontWeight="900" fontFamily="sans-serif">$1</text>
                {/* Shiny glint */}
                <circle cx="-10" cy="-10" r="4.5" fill="#FFFFFF" opacity="0.9" />
              </g>
            </g>
          ) : pose === "wheeling_cart" ? (
            <g stroke="#111116" strokeWidth="16" strokeLinecap="round" strokeLinejoin="round" fill="none">
              {/* Both arms pushing hand truck handle */}
              <path d="M 180 315 L 140 385 L 100 405" />
              <path d="M 300 315 L 240 385 L 120 410" />
              <line x1="100" y1="395" x2="130" y2="415" stroke="#94A3B8" strokeWidth="12" />
            </g>
          ) : pose === "typing" ? (
            <g stroke="#111116" strokeWidth="16" strokeLinecap="round" strokeLinejoin="round" fill="none">
              <path d="M 180 315 L 200 375 L 230 410" />
              <path d="M 300 315 L 280 375 L 250 410" />
            </g>
          ) : (
            <g stroke="#111116" strokeWidth="16" strokeLinecap="round" strokeLinejoin="round" fill="none">
              <path d="M 175 305 L 155 380 L 200 430" />
              <path d="M 305 305 L 325 380 L 280 430" />
            </g>
          )}
        </g>

        {/* --- HEAD & FACE (Oversized Stylized Light Face #F8F6F2) --- */}
        <g transform={`translate(240, ${210 + breath * 0.4 + headBob})`} filter="url(#char-shadow)">
          {/* Base Face Contour */}
          <rect
            x="-70"
            y="-80"
            width="140"
            height="150"
            rx="56"
            fill="#F8F6F2"
            stroke="#111114"
            strokeWidth="10"
          />

          {/* BASEBALL CAP (Dark Charcoal #111116) */}
          <path
            d="M -75 -40 C -75 -105 75 -105 75 -40 L 80 -25 L -80 -25 Z"
            fill="#111116"
            stroke="#111114"
            strokeWidth="10"
          />
          {/* Cap Visor Brim */}
          <path
            d="M -80 -25 Q 0 -45 105 -18 L 95 -7 Q 0 -30 -80 -13 Z"
            fill="#1A1C22"
            stroke="#111114"
            strokeWidth="7"
          />

          {/* --- EXPRESSIONS --- */}
          {expression === "scheming_smirk" ? (
            <g>
              {/* Eyebrows */}
              <path d="M -48 -8 L -18 -19" stroke="#111114" strokeWidth="7" strokeLinecap="round" />
              <path d="M 18 -14 L 48 -5" stroke="#111114" strokeWidth="7" strokeLinecap="round" />
              {/* Eyes */}
              <circle cx="-32" cy="7" r="9" fill="#111114" />
              <circle cx="32" cy="7" r="9" fill="#111114" />
              {/* Sly Smirk */}
              <path d="M -14 38 Q 16 38 32 26" fill="none" stroke="#111114" strokeWidth="7" strokeLinecap="round" />
            </g>
          ) : expression === "wide_shock" || expression === "panicked_stare" ? (
            <g>
              <path d="M -52 -20 Q -32 -35 -16 -20" fill="none" stroke="#111114" strokeWidth="7" strokeLinecap="round" />
              <path d="M 16 -20 Q 32 -35 52 -20" fill="none" stroke="#111114" strokeWidth="7" strokeLinecap="round" />
              <circle cx="-32" cy="5" r="15" fill="#FFFFFF" stroke="#111114" strokeWidth="6" />
              <circle cx="-32" cy="5" r="6" fill="#111114" />
              <circle cx="32" cy="5" r="15" fill="#FFFFFF" stroke="#111114" strokeWidth="6" />
              <circle cx="32" cy="5" r="6" fill="#111114" />
              <ellipse cx="0" cy="42" rx="15" ry="20" fill="#111114" />
              <path d="M 52 -12 Q 62 6 56 16 Q 46 16 46 6 Z" fill="#60A5FA" stroke="#1E40AF" strokeWidth="2.5" />
            </g>
          ) : expression === "focused_typing" ? (
            <g>
              <path d="M -48 -6 L -18 3" stroke="#111114" strokeWidth="7" strokeLinecap="round" />
              <path d="M 18 3 L 48 -6" stroke="#111114" strokeWidth="7" strokeLinecap="round" />
              <circle cx="-32" cy="14" r="8" fill="#111114" />
              <circle cx="32" cy="14" r="8" fill="#111114" />
              <line x1="-18" y1="38" x2="18" y2="38" stroke="#111114" strokeWidth="7" strokeLinecap="round" />
            </g>
          ) : expression === "triumphant" ? (
            <g>
              <path d="M -48 -16 Q -32 -25 -18 -16" fill="none" stroke="#111114" strokeWidth="7" strokeLinecap="round" />
              <path d="M 18 -16 Q 32 -25 48 -16" fill="none" stroke="#111114" strokeWidth="7" strokeLinecap="round" />
              <path d="M -44 9 Q -32 -2 -20 9" fill="none" stroke="#111114" strokeWidth="7" strokeLinecap="round" />
              <path d="M 20 9 Q 32 -2 44 9" fill="none" stroke="#111114" strokeWidth="7" strokeLinecap="round" />
              <path d="M -26 32 Q 0 58 26 32 Z" fill="#FFFFFF" stroke="#111114" strokeWidth="7" strokeLinejoin="round" />
            </g>
          ) : (
            <g>
              <circle cx="-32" cy="7" r="8" fill="#111114" />
              <circle cx="32" cy="7" r="8" fill="#111114" />
              <line x1="-16" y1="36" x2="16" y2="36" stroke="#111114" strokeWidth="6" strokeLinecap="round" />
            </g>
          )}

          {isBlinking && (
            <g>
              <line x1="-46" y1="8" x2="-18" y2="8" stroke="#111114" strokeWidth="7" strokeLinecap="round" />
              <line x1="18" y1="8" x2="46" y2="8" stroke="#111114" strokeWidth="7" strokeLinecap="round" />
            </g>
          )}
        </g>
      </svg>
    </div>
  );
};
