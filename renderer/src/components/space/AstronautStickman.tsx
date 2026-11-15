import React from "react";
import { useCurrentFrame } from "remotion";

export interface AstronautProps {
  pose?:
    | "idle_float"
    | "walk_explore"
    | "low_gravity_jump"
    | "point_sky"
    | "check_telemetry"
    | "panic_o2"
    | "crouch_sample"
    | "enter_airlock";
  expression?: "alert" | "curious" | "shock" | "focused" | "relief";
  x?: number; // 0.0 to 1.0 (horizontal center)
  y?: number; // 0.0 to 1.0 (vertical center, default ~0.50)
  scale?: number;
  facing?: "left" | "right";
  suitColor?: string; // default white #F5F6F8
  accentColor?: string; // default Electric Cyan #55D7E8
}

export const AstronautStickman: React.FC<AstronautProps> = ({
  pose = "walk_explore",
  expression = "focused",
  x = 0.5,
  y = 0.5,
  scale = 1.0,
  facing = "right",
  suitColor = "#F5F6F8",
  accentColor = "#55D7E8",
}) => {
  const frame = useCurrentFrame();

  // Low gravity float & breathing animations
  const breath = Math.sin(frame * 0.12) * 3;
  const floatY = pose === "idle_float" ? Math.sin(frame * 0.08) * 18 : 0;
  const floatRot = pose === "idle_float" ? Math.sin(frame * 0.06) * 4 : 0;

  // Mars low-gravity jump parabolic cycle (0.38g - slower, buoyant arc)
  const jumpPhase = (frame * 0.15) % Math.PI;
  const jumpY = pose === "low_gravity_jump" ? -Math.sin(jumpPhase) * 65 : 0;

  // Planetary walking cycle (low gravity bounce)
  const walkPhase = frame * 0.22;
  const legFront = Math.sin(walkPhase) * 38;
  const legBack = -Math.sin(walkPhase) * 38;
  const armFront = -Math.sin(walkPhase) * 30;
  const armBack = Math.sin(walkPhase) * 30;

  // Oxygen warning tremor
  const tremor = pose === "panic_o2" ? Math.sin(frame * 0.8) * 3 : 0;

  const flipH = facing === "left" ? -1 : 1;

  return (
    <div
      style={{
        position: "absolute",
        left: `${x * 100}%`,
        top: `${y * 100}%`,
        transform: `translate(-50%, -50%) translate(0px, ${floatY + jumpY}px) rotate(${floatRot}deg) scale(${scale}) scaleX(${flipH})`,
        width: 380,
        height: 560,
        pointerEvents: "none",
        zIndex: 35,
      }}
    >
      <svg
        viewBox="0 0 380 560"
        style={{ width: "100%", height: "100%", overflow: "visible" }}
      >
        <defs>
          {/* Astronaut Visor Gradient (Electric Cyan to Deep Space Navy) */}
          <linearGradient id="astro-visor-glow" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#55D7E8" stopOpacity="0.9" />
            <stop offset="45%" stopColor="#182744" stopOpacity="0.95" />
            <stop offset="100%" stopColor="#080B14" stopOpacity="1" />
          </linearGradient>

          {/* Golden Solar Visor Reflection */}
          <linearGradient id="astro-solar-gold" x1="20%" y1="0%" x2="80%" y2="100%">
            <stop offset="0%" stopColor="#FFD36B" stopOpacity="0.85" />
            <stop offset="60%" stopColor="#C65B45" stopOpacity="0.85" />
            <stop offset="100%" stopColor="#10182A" stopOpacity="0.95" />
          </linearGradient>

          {/* Drop shadow */}
          <filter id="astro-shadow" x="-30%" y="-30%" width="160%" height="160%">
            <feDropShadow dx="0" dy="12" stdDeviation="10" floodColor="rgba(8,11,20,0.6)" />
          </filter>
        </defs>

        {/* --- LIFE SUPPORT BACKPACK (Mounted behind character) --- */}
        <g transform={`translate(${112 + tremor}, ${205 + breath})`}>
          {/* Main White PLSS Backpack Unit */}
          <rect
            x="0"
            y="0"
            width="52"
            height="130"
            rx="12"
            fill={suitColor}
            stroke="#080B14"
            strokeWidth="6"
          />
          {/* Oxygen Cylinder Caps */}
          <rect x="6" y="-12" width="18" height="15" rx="5" fill="#536780" stroke="#080B14" strokeWidth="4" />
          <rect x="28" y="-12" width="18" height="15" rx="5" fill="#536780" stroke="#080B14" strokeWidth="4" />
          {/* Status LED on Backpack */}
          <circle cx="26" cy="20" r="4" fill={pose === "panic_o2" ? "#C65B45" : "#7BD69A"} />

          {/* Flexible Oxygen Supply Tubes looping into helmet */}
          <path
            d="M 12 12 C -8 10, -10 -40, 45 -45"
            fill="none"
            stroke="#536780"
            strokeWidth="6"
            strokeLinecap="round"
          />
          <path
            d="M 38 12 C 60 10, 65 -40, 52 -45"
            fill="none"
            stroke="#536780"
            strokeWidth="6"
            strokeLinecap="round"
          />
        </g>

        {/* --- STICKMAN LEGS (Clean Black Lines, strokeWidth 10px) --- */}
        <g stroke="#080B14" strokeWidth="10" strokeLinecap="round" strokeLinejoin="round" fill="none">
          {pose === "walk_explore" ? (
            <>
              {/* Buoyant low-gravity planetary walk */}
              <path d={`M 175 350 L ${155 + legFront} 425 L ${140 + legFront * 1.2} 490`} />
              <path d={`M 205 350 L ${225 + legBack} 425 L ${240 + legBack * 1.2} 490`} />
            </>
          ) : pose === "low_gravity_jump" ? (
            <>
              {/* Tucked legs in mid-jump floating above surface */}
              <path d="M 175 340 L 140 385 L 175 435" />
              <path d="M 205 340 L 235 390 L 210 445" />
            </>
          ) : pose === "crouch_sample" ? (
            <>
              {/* Kneeling to examine Mars regolith */}
              <path d="M 165 350 L 125 415 L 165 485" />
              <path d="M 215 350 L 250 410 L 230 485" />
            </>
          ) : (
            <>
              {/* Balanced standing stance */}
              <path d="M 175 350 L 160 425 L 150 490" />
              <path d="M 205 350 L 220 425 L 230 490" />
            </>
          )}
        </g>

        {/* --- CHUNKY MOON EXPLORATION BOOTS --- */}
        <g fill="#080B14">
          {pose === "walk_explore" ? (
            <>
              <ellipse cx={135 + legFront * 1.2} cy={490} rx={18} ry={9} />
              <ellipse cx={245 + legBack * 1.2} cy={490} rx={18} ry={9} />
              {/* Boot tread stripes */}
              <rect x={122 + legFront * 1.2} y="492" width="26" height="5" rx="2" fill="#536780" />
              <rect x={232 + legBack * 1.2} y="492" width="26" height="5" rx="2" fill="#536780" />
            </>
          ) : pose === "low_gravity_jump" ? (
            <>
              <ellipse cx={175} cy={435} rx={16} ry={8} />
              <ellipse cx={210} cy={445} rx={16} ry={8} />
            </>
          ) : (
            <>
              <ellipse cx={145} cy={490} rx={18} ry={9} />
              <ellipse cx={235} cy={490} rx={18} ry={9} />
              <rect x="132" y="492" width="26" height="5" rx="2" fill="#536780" />
              <rect x="222" y="492" width="26" height="5" rx="2" fill="#536780" />
            </>
          )}
        </g>

        {/* --- SPACESUIT TORSO & LIFE SUPPORT CHEST UNIT --- */}
        <g transform={`translate(${tremor}, ${breath})`} filter="url(#astro-shadow)">
          {/* Main White Spacesuit Torso */}
          <path
            d="M 155,210 L 225,210 L 235,350 L 145,350 Z"
            fill={suitColor}
            stroke="#080B14"
            strokeWidth="7"
            strokeLinejoin="round"
          />

          {/* Mission Stripes on shoulders (Electric Cyan #55D7E8) */}
          <rect x="148" y="218" width="7" height="35" rx="2" fill={accentColor} />
          <rect x="225" y="218" width="7" height="35" rx="2" fill={accentColor} />

          {/* Chest Life-Support Control Module */}
          <rect
            x="165"
            y="240"
            width="50"
            height="65"
            rx="8"
            fill="#182744"
            stroke="#080B14"
            strokeWidth="4"
          />

          {/* Chest Telemetry Screen (O2 Bar & Status) */}
          <rect x="171" y="247" width="38" height="18" rx="3" fill="#080B14" />
          <line
            x1="174"
            y1="256"
            x2={pose === "panic_o2" ? "180" : "205"}
            y2="256"
            stroke={pose === "panic_o2" ? "#C65B45" : "#7BD69A"}
            strokeWidth="3.5"
            strokeLinecap="round"
          />
          {/* Small status dials */}
          <circle cx="177" cy="278" r="4" fill="#55D7E8" />
          <circle cx="190" cy="278" r="4" fill="#FFD36B" />
          <circle cx="203" cy="278" r="4" fill={pose === "panic_o2" ? "#C65B45" : "#536780"} />
        </g>

        {/* --- SPACESUIT ARMS & PROPS DEPENDING ON POSE --- */}
        <g stroke="#080B14" strokeWidth="10" strokeLinecap="round" strokeLinejoin="round" fill="none">
          {pose === "walk_explore" ? (
            <>
              {/* Natural swinging exploration arms */}
              <path d={`M 155,220 L ${130 + armFront} 275 L ${115 + armFront * 1.3} 325`} />
              <path d={`M 225,220 L ${250 + armBack} 270 L ${270 + armBack * 1.3} 320`} />
              {/* Glove cuffs */}
              <circle cx={115 + armFront * 1.3} cy={325} r="8" fill="#536780" stroke="#080B14" strokeWidth="4" />
              <circle cx={270 + armBack * 1.3} cy={320} r="8" fill="#536780" stroke="#080B14" strokeWidth="4" />
            </>
          ) : pose === "point_sky" ? (
            <>
              {/* Left hand relaxed, right hand pointing high to moons/stars */}
              <path d="M 155,220 L 140,275 L 145,330" />
              <path d="M 225,220 L 275,170 L 315,115" />
              {/* Pointing glove */}
              <circle cx="315" cy="115" r="9" fill={accentColor} stroke="#080B14" strokeWidth="4" />
            </>
          ) : pose === "check_telemetry" ? (
            <>
              {/* Looking at wrist computer */}
              <path d="M 155,220 L 145,280 L 155,330" />
              <path d="M 225,220 L 265,260 L 235,270" />
              {/* Wrist Telemetry HUD Hologram */}
              <g transform="translate(240, 250)" strokeWidth="0">
                <rect x="-10" y="-8" width="26" height="18" rx="3" fill="#182744" stroke="#080B14" strokeWidth="3" />
                {/* Holographic Projection Beam */}
                <polygon points="3,-8 40,-35 40,-5 3,-2" fill="#55D7E8" opacity="0.35" />
                <rect x="40" y="-40" width="70" height="38" rx="4" fill="#080B14" stroke="#55D7E8" strokeWidth="2" />
                <text x="45" y="-25" fill="#55D7E8" fontSize="9" fontWeight="900" fontFamily="monospace">O2: 78%</text>
                <text x="45" y="-12" fill="#FFD36B" fontSize="8" fontWeight="800" fontFamily="monospace">-63°C</text>
              </g>
            </>
          ) : pose === "panic_o2" ? (
            <>
              {/* Hands grasping helmet / oxygen valves in alarm */}
              <path d="M 155,220 L 135,180 L 150,145" />
              <path d="M 225,220 L 245,180 L 230,145" />
              <circle cx="150" cy="145" r="9" fill="#C65B45" stroke="#080B14" strokeWidth="4" />
              <circle cx="230" cy="145" r="9" fill="#C65B45" stroke="#080B14" strokeWidth="4" />
            </>
          ) : pose === "crouch_sample" ? (
            <>
              {/* Hand holding scientific geology rock scanner */}
              <path d="M 155,220 L 140,270 L 145,320" />
              <path d="M 225,220 L 255,290 L 275,360" />
              {/* Geological laser scanner */}
              <g transform="translate(275, 360)" strokeWidth="0">
                <rect x="-8" y="-5" width="24" height="12" rx="3" fill="#536780" stroke="#080B14" strokeWidth="2" />
                {/* Sampling beam down to ground */}
                <line x1="16" y1="0" x2="35" y2="45" stroke="#55D7E8" strokeWidth="3" strokeDasharray="4 3" />
              </g>
            </>
          ) : pose === "enter_airlock" ? (
            <>
              {/* Reaching forward to open the habitat airlock wheel */}
              <path d="M 155,220 L 175,260 L 220,270" />
              <path d="M 225,220 L 270,240 L 310,230" />
            </>
          ) : (
            <>
              {/* Standard idle arms */}
              <path d="M 155,220 L 140,275 L 145,330" />
              <path d="M 225,220 L 240,275 L 235,330" />
            </>
          )}
        </g>

        {/* --- SPACESUIT HELMET & VISOR --- */}
        <g transform={`translate(${190 + tremor}, ${145 + breath * 0.5})`} filter="url(#astro-shadow)">
          {/* Outer Spherical White Helmet */}
          <circle
            cx="0"
            cy="0"
            r="44"
            fill={suitColor}
            stroke="#080B14"
            strokeWidth="7"
          />

          {/* Helmet Neck Ring / Lock Collar */}
          <ellipse cx="0" cy="42" rx="34" ry="9" fill="#536780" stroke="#080B14" strokeWidth="5" />

          {/* Bubble Gold / Electric Cyan Visor */}
          <ellipse
            cx="6"
            cy="2"
            rx="32"
            ry="28"
            fill="url(#astro-visor-glow)"
            stroke="#080B14"
            strokeWidth="4"
          />

          {/* Visor Glint & Curved Specular Reflection */}
          <path
            d="M -16 -16 Q 0 -26 22 -14"
            fill="none"
            stroke="#FFFFFF"
            strokeWidth="4"
            strokeLinecap="round"
            opacity="0.75"
          />

          {/* Stickman Eyes visible through transparent visor */}
          {expression === "shock" ? (
            <g fill="#F5F6F8">
              <circle cx="-2" cy="0" r="6" />
              <circle cx="16" cy="0" r="6" />
              <circle cx="-1" cy="0" r="2.5" fill="#080B14" />
              <circle cx="17" cy="0" r="2.5" fill="#080B14" />
            </g>
          ) : expression === "curious" ? (
            <g fill="#F5F6F8">
              <circle cx="-2" cy="-2" r="4.5" />
              <circle cx="16" cy="-2" r="4.5" />
            </g>
          ) : (
            <g fill="#F5F6F8">
              <circle cx="-2" cy="2" r="4" />
              <circle cx="16" cy="2" r="4" />
            </g>
          )}

          {/* Helmet Torch Light Cone (Active in dark environments) */}
          <circle cx="28" cy="-15" r="4" fill="#FFD36B" stroke="#080B14" strokeWidth="2" />
        </g>
      </svg>
    </div>
  );
};
