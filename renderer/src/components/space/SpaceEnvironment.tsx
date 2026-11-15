import React from "react";
import { useCurrentFrame } from "remotion";

interface SpaceEnvironmentProps {
  environment: string;
  planet?: "mars" | "moon" | "jupiter" | "venus" | "titan" | "deep_space";
  sceneId: number;
}

/**
 * Handcrafted 2D Space & Planetary Environment (v2.2 Cinematic Edition)
 * - Pure cinematic storytelling: Zero PowerPoint slides, zero comparison tables, zero label boxes
 * - Animated elements: rotating radar, rock-drilling laser sparks, boiling vacuum chamber, rocket liftoff
 * - Clean visual hierarchy with zero text collisions
 */
export const SpaceEnvironment: React.FC<SpaceEnvironmentProps> = ({
  environment,
  planet = "mars",
  sceneId,
}) => {
  const frame = useCurrentFrame();

  // Strict Editorial Palette
  const PAPER_CREAM = "#F4EFE5";
  const INK_CHARCOAL = "#242B35";
  const DUSTY_CORAL = "#C86D52";
  const MUTED_BLUE = "#527A9B";
  const WARM_GOLD = "#D5AA62";
  const STONE_GREY = "#A6A18F";
  const SAGE_GREEN = "#768C79";
  const SAND_BEIGE = "#D8C5AA";
  const SPACE_BLACK = "#0A0D14";

  // Dynamic animations
  const starTwinkle = Math.sin(frame * 0.08) * 0.25 + 0.75;
  const sunPulse = Math.sin(frame * 0.04) * 5;
  const satelliteX = 260 + Math.sin(frame * 0.02) * 25;
  const satelliteY = 960 + Math.cos(frame * 0.02) * 15;
  const satelliteRot = Math.sin(frame * 0.015) * 4;
  const dishRotation = (frame * 1.8) % 360;
  const dustDrift = (frame * 16) % 1500;
  const stormWinds = (frame * 42) % 1800;
  const rocketLift = Math.min(frame * 16, 750);
  const flameFlicker = (frame % 4) * 8;
  const laserPulse = frame % 8 < 5;
  const boilingBubble = Math.sin(frame * 0.6) * 6;

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        backgroundColor: SPACE_BLACK,
        overflow: "hidden",
      }}
    >
      <svg
        viewBox="0 0 1080 1920"
        style={{ width: "100%", height: "100%" }}
        preserveAspectRatio="xMidYMid slice"
      >
        <defs>
          {/* Deep Space Radial Gradient */}
          <radialGradient id="deep-space" cx="50%" cy="35%" r="75%">
            <stop offset="0%" stopColor="#1B2330" />
            <stop offset="55%" stopColor="#10151E" />
            <stop offset="100%" stopColor="#07090D" />
          </radialGradient>

          {/* Mars Atmospheric Sky Gradient */}
          <linearGradient id="mars-sky" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#151A22" />
            <stop offset="35%" stopColor="#2D3542" />
            <stop offset="70%" stopColor="#5E433E" />
            <stop offset="100%" stopColor="#9E4D38" />
          </linearGradient>

          {/* Mars Planet Sphere Gradient */}
          <radialGradient id="mars-globe" cx="35%" cy="35%" r="65%">
            <stop offset="0%" stopColor="#E27457" />
            <stop offset="50%" stopColor="#BD5338" />
            <stop offset="85%" stopColor="#7E2C1E" />
            <stop offset="100%" stopColor="#350E07" />
          </radialGradient>

          {/* Sun Glow */}
          <radialGradient id="sun-corona" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#FFFFFF" stopOpacity="1" />
            <stop offset="30%" stopColor="#FFF2D1" stopOpacity="0.95" />
            <stop offset="60%" stopColor={WARM_GOLD} stopOpacity="0.6" />
            <stop offset="85%" stopColor={DUSTY_CORAL} stopOpacity="0.25" />
            <stop offset="100%" stopColor="transparent" stopOpacity="0" />
          </radialGradient>

          {/* Rocket Exhaust Flame */}
          <linearGradient id="rocket-flame" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#FFFFFF" />
            <stop offset="25%" stopColor="#FFF1B8" />
            <stop offset="55%" stopColor="#FF7A33" />
            <stop offset="85%" stopColor={DUSTY_CORAL} />
            <stop offset="100%" stopColor="transparent" />
          </linearGradient>

          {/* Solar Panel Texture */}
          <linearGradient id="solar-cell" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#2A4B6B" />
            <stop offset="100%" stopColor="#152638" />
          </linearGradient>

          {/* Martian Dunes Gradient */}
          <linearGradient id="dunes-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor={DUSTY_CORAL} />
            <stop offset="50%" stopColor="#AD533B" />
            <stop offset="100%" stopColor="#6E2F20" />
          </linearGradient>
        </defs>

        {/* ========================================================================= */}
        {/* SCENE 1: ORBITAL ARRIVAL (PLANET MARS, SUN, SATELLITE & CRUISE CRAFT)     */}
        {/* ========================================================================= */}
        {sceneId === 1 && (
          <g>
            <rect width="1080" height="1920" fill="url(#deep-space)" />

            {/* Twinkling Starfield */}
            <g fill="#FFFFFF">
              {[
                [100, 140, 2], [240, 80, 1.5], [420, 200, 2.5], [760, 130, 2],
                [940, 240, 1.5], [120, 380, 2], [300, 520, 1.5], [80, 840, 2.5],
                [190, 1140, 1.5], [870, 1280, 2], [990, 880, 2.5], [820, 620, 1.5],
                [480, 1420, 2], [310, 1620, 1.5], [760, 1660, 2.5], [130, 1490, 2]
              ].map(([sx, sy, sr], i) => (
                <circle key={i} cx={sx} cy={sy} r={sr} opacity={i % 2 === 0 ? starTwinkle : 0.85} />
              ))}
            </g>

            {/* THE SUN (Glowing Solar Corona in Space) */}
            <g transform="translate(180, 280)">
              <circle cx="0" cy="0" r={170 + sunPulse} fill="url(#sun-corona)" />
              <circle cx="0" cy="0" r="58" fill="#FFFCE8" stroke={WARM_GOLD} strokeWidth="4" />
              {[0, 45, 90, 135, 180, 225, 270, 315].map((deg, idx) => (
                <line
                  key={idx}
                  x1="0"
                  y1="0"
                  x2={Math.cos((deg * Math.PI) / 180) * 100}
                  y2={Math.sin((deg * Math.PI) / 180) * 100}
                  stroke={WARM_GOLD}
                  strokeWidth="3.5"
                  strokeLinecap="round"
                  opacity="0.7"
                />
              ))}
            </g>

            {/* PLANET MARS GLOBE (Detailed High-Resolution 2D Sphere) */}
            <g transform="translate(680, 960)">
              {/* Atmospheric Limb Glow */}
              <circle cx="0" cy="0" r="375" fill="none" stroke="#6893B8" strokeWidth="14" opacity="0.65" />
              <circle cx="0" cy="0" r="368" fill="none" stroke={DUSTY_CORAL} strokeWidth="7" opacity="0.45" />

              {/* Main Planet Sphere */}
              <circle cx="0" cy="0" r="360" fill="url(#mars-globe)" stroke={INK_CHARCOAL} strokeWidth="8" />

              {/* North Polar Ice Cap (Planum Boreum) */}
              <path
                d="M -110 -310 Q 0 -360 110 -310 Q 60 -270 -30 -280 Q -90 -290 -110 -310 Z"
                fill="#F8F6F0"
                stroke={INK_CHARCOAL}
                strokeWidth="3.5"
              />

              {/* Valles Marineris Canyon System */}
              <path
                d="M -160 -40 Q -40 20 140 -20 Q 220 10 260 -5 Q 210 25 130 15 Q -60 45 -160 -40 Z"
                fill="#4D160E"
                stroke={INK_CHARCOAL}
                strokeWidth="4"
              />
              <path
                d="M -220 80 Q -140 140 -60 110 Q 20 170 -40 210 Q -180 230 -220 80 Z"
                fill="#44130C"
                stroke={INK_CHARCOAL}
                strokeWidth="3"
              />

              {/* Olympus Mons Volcano Shield */}
              <ellipse cx="-130" cy="-140" rx="48" ry="32" fill="#782E20" stroke={INK_CHARCOAL} strokeWidth="3" />
              <ellipse cx="-130" cy="-140" rx="16" ry="10" fill="#3D120A" />
            </g>

            {/* ORBITING SCIENTIFIC SATELLITE (Drifting in orbit) */}
            <g transform={`translate(${satelliteX}, ${satelliteY}) rotate(${satelliteRot})`}>
              {/* Satellite Body (Gold-foil bus) */}
              <rect x="-40" y="-35" width="80" height="70" rx="8" fill={WARM_GOLD} stroke={INK_CHARCOAL} strokeWidth="5" />
              <rect x="-30" y="-25" width="60" height="50" rx="4" fill="#B88A3B" />
              <line x1="-30" y1="0" x2="30" y2="0" stroke={INK_CHARCOAL} strokeWidth="3" />

              {/* High-Gain Parabolic Dish Antenna */}
              <path d="M 0 -35 Q 25 -75 55 -60 Q 25 -45 0 -35 Z" fill="#E8E2D5" stroke={INK_CHARCOAL} strokeWidth="4" />
              <line x1="25" y1="-55" x2="42" y2="-75" stroke={INK_CHARCOAL} strokeWidth="3" />
              <circle cx="44" cy="-77" r="4" fill={DUSTY_CORAL} />

              {/* Left Multi-Panel Solar Array */}
              <g transform="translate(-40, 0)">
                <line x1="0" y1="0" x2="-140" y2="0" stroke={INK_CHARCOAL} strokeWidth="6" />
                <rect x="-140" y="-45" width="130" height="90" rx="6" fill="url(#solar-cell)" stroke={INK_CHARCOAL} strokeWidth="4" />
                <line x1="-97" y1="-45" x2="-97" y2="45" stroke="#4878A4" strokeWidth="2" />
                <line x1="-54" y1="-45" x2="-54" y2="45" stroke="#4878A4" strokeWidth="2" />
                <line x1="-140" y1="-15" x2="-10" y2="-15" stroke="#4878A4" strokeWidth="2" />
                <line x1="-140" y1="15" x2="-10" y2="15" stroke="#4878A4" strokeWidth="2" />
              </g>

              {/* Right Multi-Panel Solar Array */}
              <g transform="translate(40, 0)">
                <line x1="0" y1="0" x2="140" y2="0" stroke={INK_CHARCOAL} strokeWidth="6" />
                <rect x="10" y="-45" width="130" height="90" rx="6" fill="url(#solar-cell)" stroke={INK_CHARCOAL} strokeWidth="4" />
                <line x1="53" y1="-45" x2="53" y2="45" stroke="#4878A4" strokeWidth="2" />
                <line x1="96" y1="-45" x2="96" y2="45" stroke="#4878A4" strokeWidth="2" />
                <line x1="10" y1="-15" x2="140" y2="-15" stroke="#4878A4" strokeWidth="2" />
                <line x1="10" y1="15" x2="140" y2="15" stroke="#4878A4" strokeWidth="2" />
              </g>

              {/* Sensor Boom */}
              <line x1="0" y1="35" x2="0" y2="90" stroke={INK_CHARCOAL} strokeWidth="4" />
              <circle cx="0" cy="94" r="6" fill={SAGE_GREEN} stroke={INK_CHARCOAL} strokeWidth="3" />
            </g>

            {/* INTERPLANETARY CRUISE SPACECRAFT (Upper right) */}
            <g transform="translate(720, 440) scale(0.9)">
              <rect x="-80" y="-22" width="160" height="44" rx="14" fill="#EAE4D8" stroke={INK_CHARCOAL} strokeWidth="5" />
              <path d="M 50 -12 Q 80 0 50 12 Z" fill={MUTED_BLUE} stroke={INK_CHARCOAL} strokeWidth="3.5" />
              <polygon points="-80,-18 -115,-30 -115,30 -80,18" fill="#5A6678" stroke={INK_CHARCOAL} strokeWidth="4" />
              <ellipse cx="-120" cy="0" rx="15" ry="8" fill="#7FB7E0" opacity="0.8" />
              <rect x="-35" y="-55" width="70" height="30" rx="4" fill="#D5AA62" stroke={INK_CHARCOAL} strokeWidth="3" />
              <rect x="-35" y="25" width="70" height="30" rx="4" fill="#D5AA62" stroke={INK_CHARCOAL} strokeWidth="3" />
            </g>
          </g>
        )}

        {/* ========================================================================= */}
        {/* SCENE 2: SURFACE TOUCHDOWN & 3-STORY LANDER SPACECRAFT                    */}
        {/* ========================================================================= */}
        {sceneId === 2 && (
          <g>
            <rect width="1080" height="1920" fill="url(#mars-sky)" />

            {/* Sun & Moon */}
            <circle cx="820" cy="380" r="42" fill="#FFE8BF" stroke={WARM_GOLD} strokeWidth="3" />
            <ellipse cx="640" cy="280" rx="18" ry="12" fill="#A89F91" stroke={INK_CHARCOAL} strokeWidth="2.5" />

            {/* Distant Crater Horizons */}
            <polygon
              points="-50,960 180,880 440,940 760,860 1130,930 1130,1350 -50,1350"
              fill="#522920"
              stroke={INK_CHARCOAL}
              strokeWidth="5"
            />

            {/* Midground Martian Dunes */}
            <path
              d="M -40 1120 Q 280 1060 620 1130 Q 920 1180 1120 1100 L 1120 1480 L -40 1480 Z"
              fill="#853C2C"
              stroke={INK_CHARCOAL}
              strokeWidth="6"
            />

            {/* 3-STORY EXPLORATION LANDER SPACECRAFT (Positioned on the left) */}
            <g transform="translate(240, 1020)">
              {/* Main Fuselage */}
              <rect x="-85" y="-360" width="170" height="340" rx="20" fill="#EAE4D8" stroke={INK_CHARCOAL} strokeWidth="7" />
              <path d="M -85 -360 Q 0 -440 85 -360 Z" fill="#D8D0C2" stroke={INK_CHARCOAL} strokeWidth="6" />
              <rect x="-95" y="-20" width="190" height="24" rx="6" fill="#3D4552" stroke={INK_CHARCOAL} strokeWidth="5" />
              <polygon points="-25,4 -45,45 45,45 25,4" fill="#242B35" stroke={INK_CHARCOAL} strokeWidth="4" />

              {/* Left Landing Leg */}
              <path d="M -85 -30 L -170 65 L -165 75 L -80 -10" fill="#525E70" stroke={INK_CHARCOAL} strokeWidth="5" />
              <ellipse cx="-175" cy="72" rx="35" ry="12" fill="#343C47" stroke={INK_CHARCOAL} strokeWidth="4.5" />
              <line x1="-85" y1="-140" x2="-150" y2="40" stroke={INK_CHARCOAL} strokeWidth="4" />

              {/* Right Landing Leg */}
              <path d="M 85 -30 L 170 65 L 165 75 L 80 -10" fill="#525E70" stroke={INK_CHARCOAL} strokeWidth="5" />
              <ellipse cx="175" cy="72" rx="35" ry="12" fill="#343C47" stroke={INK_CHARCOAL} strokeWidth="4.5" />
              <line x1="85" y1="-140" x2="150" y2="40" stroke={INK_CHARCOAL} strokeWidth="4" />

              {/* Crew Exit Airlock & Deployed Ladder */}
              <rect x="-26" y="-120" width="52" height="75" rx="8" fill="#2C3542" stroke={INK_CHARCOAL} strokeWidth="4" />
              <line x1="-16" y1="-45" x2="-16" y2="70" stroke={INK_CHARCOAL} strokeWidth="4" />
              <line x1="16" y1="-45" x2="16" y2="70" stroke={INK_CHARCOAL} strokeWidth="4" />
              {[-30, -10, 10, 30, 50].map((ly, idx) => (
                <line key={idx} x1="-16" y1={ly} x2="16" y2={ly} stroke={INK_CHARCOAL} strokeWidth="3.5" />
              ))}

              {/* Antenna Mast */}
              <line x1="0" y1="-430" x2="0" y2="-490" stroke={INK_CHARCOAL} strokeWidth="4.5" />
              <path d="M -22 -490 Q 0 -515 22 -490 Z" fill="#FFFFFF" stroke={INK_CHARCOAL} strokeWidth="3" />
            </g>

            {/* Parabolic Low-Gravity Jump Trajectory Arc (Clean physics curve - NO overlapping boxes) */}
            <path
              d="M 380 1240 Q 640 760 900 1240"
              fill="none"
              stroke={WARM_GOLD}
              strokeWidth="5"
              strokeDasharray="14 10"
              opacity="0.85"
            />

            {/* Foreground Dunes */}
            <path
              d="M -40 1220 Q 280 1160 580 1230 Q 860 1290 1120 1210 L 1120 1920 L -40 1920 Z"
              fill="url(#dunes-gradient)"
              stroke={INK_CHARCOAL}
              strokeWidth="9"
            />
            <g fill="#4A1E15" stroke={INK_CHARCOAL} strokeWidth="5" strokeLinejoin="round">
              <ellipse cx="490" cy="1260" rx="34" ry="16" />
              <ellipse cx="940" cy="1280" rx="44" ry="20" />
            </g>
          </g>
        )}

        {/* ========================================================================= */}
        {/* SCENE 3: MARS SCIENCE ROVER & BOILING BLOOD VACUUM EXPERIMENT              */}
        {/* (Pure action & cinematic science - ZERO PowerPoint comparison tables)     */}
        {/* ========================================================================= */}
        {sceneId === 3 && (
          <g>
            <rect width="1080" height="1920" fill="url(#mars-sky)" />

            {/* Sun in distant haze */}
            <circle cx="780" cy="360" r="40" fill="#FFF0D0" stroke={WARM_GOLD} strokeWidth="3" />

            {/* Towering Martian Rock Outcrops */}
            <polygon
              points="-40,880 160,780 340,840 520,740 740,820 1120,760 1120,1350 -40,1350"
              fill="#5A261C"
              stroke={INK_CHARCOAL}
              strokeWidth="6"
            />

            {/* Bedrock Ridge with Stratified Mineral Layers */}
            <path
              d="M -40 1060 Q 260 990 640 1060 Q 940 1110 1120 1040 L 1120 1450 L -40 1450 Z"
              fill="#7E3728"
              stroke={INK_CHARCOAL}
              strokeWidth="6"
            />

            {/* =============================================================== */}
            {/* THE AUTONOMOUS MARS SCIENCE ROVER (Drilling bedrock with laser)  */}
            {/* =============================================================== */}
            <g transform="translate(360, 1140)">
              {/* Chassis */}
              <rect x="-110" y="-70" width="220" height="80" rx="16" fill="#DCD5C8" stroke={INK_CHARCOAL} strokeWidth="6" />
              <rect x="-85" y="-55" width="170" height="35" rx="8" fill="#525E70" />

              {/* Mast & Pan-Cam */}
              <line x1="-60" y1="-70" x2="-60" y2="-170" stroke={INK_CHARCOAL} strokeWidth="6" strokeLinecap="round" />
              <rect x="-85" y="-200" width="50" height="32" rx="6" fill="#3D4552" stroke={INK_CHARCOAL} strokeWidth="4" />
              <circle cx="-72" cy="-184" r="7" fill={MUTED_BLUE} stroke={INK_CHARCOAL} strokeWidth="2.5" />
              <circle cx="-48" cy="-184" r="7" fill={MUTED_BLUE} stroke={INK_CHARCOAL} strokeWidth="2.5" />

              {/* High Gain Dish */}
              <line x1="50" y1="-70" x2="50" y2="-130" stroke={INK_CHARCOAL} strokeWidth="5" />
              <path d="M 30 -130 Q 50 -155 70 -130 Z" fill="#FFFFFF" stroke={INK_CHARCOAL} strokeWidth="3" />

              {/* Robotic Arm with Spectrometer Drill */}
              <g transform="translate(-110, -20)">
                <line x1="0" y1="0" x2="-70" y2="40" stroke={INK_CHARCOAL} strokeWidth="7" strokeLinecap="round" />
                <line x1="-70" y1="40" x2="-125" y2="85" stroke={INK_CHARCOAL} strokeWidth="6" strokeLinecap="round" />
                <rect x="-140" y="80" width="30" height="20" rx="4" fill="#6E7B8B" stroke={INK_CHARCOAL} strokeWidth="3" />

                {/* Laser Spectrometer Beam (Active pulsing laser into Martian rock) */}
                {laserPulse && (
                  <line x1="-125" y1="100" x2="-125" y2="135" stroke="#FF2B2B" strokeWidth="5" strokeLinecap="round" />
                )}
                {/* Laser Sparks */}
                {laserPulse && (
                  <g fill="#FFA834">
                    <circle cx="-130" cy="130" r="3" />
                    <circle cx="-120" cy="128" r="3.5" />
                    <circle cx="-125" cy="124" r="2.5" />
                  </g>
                )}
              </g>

              {/* Rocker-Bogie Suspension & 6 Wheels */}
              <line x1="-80" y1="10" x2="-120" y2="70" stroke={INK_CHARCOAL} strokeWidth="6" />
              <line x1="0" y1="10" x2="0" y2="70" stroke={INK_CHARCOAL} strokeWidth="6" />
              <line x1="80" y1="10" x2="120" y2="70" stroke={INK_CHARCOAL} strokeWidth="6" />

              {[-120, 0, 120].map((wx, widx) => (
                <g key={widx} transform={`translate(${wx}, 85)`}>
                  <circle cx="0" cy="0" r="28" fill="#3D4552" stroke={INK_CHARCOAL} strokeWidth="5" />
                  <circle cx="0" cy="0" r="14" fill="#A89F91" stroke={INK_CHARCOAL} strokeWidth="3" />
                  {[0, 60, 120, 180, 240, 300].map((deg, ti) => (
                    <line
                      key={ti}
                      x1={Math.cos((deg * Math.PI) / 180) * 14}
                      y1={Math.sin((deg * Math.PI) / 180) * 14}
                      x2={Math.cos((deg * Math.PI) / 180) * 28}
                      y2={Math.sin((deg * Math.PI) / 180) * 28}
                      stroke={INK_CHARCOAL}
                      strokeWidth="3"
                    />
                  ))}
                </g>
              ))}

              {/* Target Martian Bedrock Boulder being sampled */}
              <polygon points="-280,1180 -190,1120 -130,1190 -230,1230" fill="#8C3A29" stroke={INK_CHARCOAL} strokeWidth="4" />
            </g>

            {/* =============================================================== */}
            {/* SCIENTIFIC VACUUM EXPERIMENT STAND (BOILING LIQUID AT 0.006 ATM)*/}
            {/* =============================================================== */}
            <g transform="translate(860, 1080)">
              {/* Tripod Stand */}
              <line x1="0" y1="60" x2="-40" y2="150" stroke={INK_CHARCOAL} strokeWidth="5" strokeLinecap="round" />
              <line x1="0" y1="60" x2="40" y2="150" stroke={INK_CHARCOAL} strokeWidth="5" strokeLinecap="round" />
              <line x1="0" y1="60" x2="0" y2="150" stroke={INK_CHARCOAL} strokeWidth="5" strokeLinecap="round" />

              {/* Glass Vacuum Cylinder */}
              <rect x="-35" y="-120" width="70" height="180" rx="14" fill="rgba(110, 150, 180, 0.25)" stroke={INK_CHARCOAL} strokeWidth="5" />

              {/* Boiling Red Fluid (Simulating blood / water boiling at 0.006 ATM) */}
              <path d="M -32 20 Q 0 10 32 20 L 32 50 L -32 50 Z" fill={DUSTY_CORAL} />
              {/* Animated Boiling Bubbles */}
              <circle cx="-12" cy={15 + boilingBubble} r="5" fill="#FFE8E0" />
              <circle cx="14" cy={5 - boilingBubble} r="6" fill="#FFE8E0" />
              <circle cx="2" cy={-15 + boilingBubble * 1.5} r="4" fill="#FFE8E0" />

              {/* Pressure Dial on Top of Cylinder */}
              <circle cx="0" cy="-135" r="22" fill="#FFFFFF" stroke={INK_CHARCOAL} strokeWidth="4" />
              <line x1="0" y1="-135" x2="-12" y2="-140" stroke="#FF2B2B" strokeWidth="3" strokeLinecap="round" />
              <circle cx="0" cy="-135" r="4" fill={INK_CHARCOAL} />
            </g>

            {/* Foreground Dunes */}
            <path
              d="M -40 1230 Q 280 1170 580 1240 Q 860 1300 1120 1220 L 1120 1920 L -40 1920 Z"
              fill="url(#dunes-gradient)"
              stroke={INK_CHARCOAL}
              strokeWidth="9"
            />
          </g>
        )}

        {/* ========================================================================= */}
        {/* SCENE 4: BASE ALPHA HABITAT, GREENHOUSE & ROTATING COMMUNICATIONS TOWER   */}
        {/* ========================================================================= */}
        {sceneId === 4 && (
          <g>
            <rect width="1080" height="1920" fill="url(#mars-sky)" />
            <circle cx="280" cy="420" r="48" fill="#FFF2D6" stroke={WARM_GOLD} strokeWidth="4" />

            {/* Distant Hills */}
            <polygon
              points="-50,960 220,890 540,950 820,880 1130,940 1130,1350 -50,1350"
              fill="#522920"
              stroke={INK_CHARCOAL}
              strokeWidth="5"
            />
            <path
              d="M -40 1120 Q 280 1060 620 1130 Q 920 1180 1120 1100 L 1120 1450 L -40 1450 Z"
              fill="#853C2C"
              stroke={INK_CHARCOAL}
              strokeWidth="6"
            />

            {/* BASE ALPHA GEODESIC DOME SANCTUARY */}
            <g transform="translate(680, 1180)">
              <path d="M -240 0 A 240 240 0 0 1 240 0 Z" fill="#EAE4D8" stroke={INK_CHARCOAL} strokeWidth="7" />

              {/* Interior Greenhouse with illuminated hydroponic plants */}
              <path d="M -160 0 A 160 160 0 0 1 160 0 Z" fill="#D8E8D5" stroke={INK_CHARCOAL} strokeWidth="5" />
              <g fill={SAGE_GREEN} stroke={INK_CHARCOAL} strokeWidth="2.5">
                <path d="M -80 0 Q -70 -60 -40 -70 Q -30 -30 -50 0 Z" />
                <path d="M -10 0 Q 0 -80 30 -90 Q 40 -40 15 0 Z" />
                <path d="M 60 0 Q 75 -50 110 -60 Q 90 -20 80 0 Z" />
              </g>

              {/* Geodesic Structural Trusses */}
              <g stroke={INK_CHARCOAL} strokeWidth="3.5" fill="none">
                <line x1="-240" y1="0" x2="-140" y2="-120" />
                <line x1="-140" y1="-120" x2="0" y2="-240" />
                <line x1="0" y1="-240" x2="140" y2="-120" />
                <line x1="140" y1="-120" x2="240" y2="0" />
                <line x1="-140" y1="-120" x2="0" y2="-80" />
                <line x1="140" y1="-120" x2="0" y2="-80" />
                <line x1="0" y1="-80" x2="0" y2="0" />
              </g>

              {/* Pressurized Airlock Module */}
              <g transform="translate(-240, -10)">
                <rect x="-80" y="-85" width="80" height="95" rx="8" fill="#525E70" stroke={INK_CHARCOAL} strokeWidth="5" />
                <ellipse cx="-40" cy="-35" rx="24" ry="38" fill="#343C47" stroke={INK_CHARCOAL} strokeWidth="3.5" />
                <circle cx="-40" cy="-65" r="5" fill="#3DDF78" stroke={INK_CHARCOAL} strokeWidth="2" />
              </g>
            </g>

            {/* DUAL-AXIS SOLAR COLLECTOR PANEL FIELDS */}
            <g transform="translate(180, 1150)">
              <g transform="translate(0, 0)">
                <line x1="0" y1="0" x2="0" y2="60" stroke={INK_CHARCOAL} strokeWidth="6" />
                <rect x="-65" y="-55" width="130" height="60" rx="6" fill="url(#solar-cell)" stroke={INK_CHARCOAL} strokeWidth="4.5" transform="rotate(-15)" />
              </g>
              <g transform="translate(130, 20)">
                <line x1="0" y1="0" x2="0" y2="60" stroke={INK_CHARCOAL} strokeWidth="6" />
                <rect x="-65" y="-55" width="130" height="60" rx="6" fill="url(#solar-cell)" stroke={INK_CHARCOAL} strokeWidth="4.5" transform="rotate(-15)" />
              </g>
            </g>

            {/* ROTATING COMMUNICATIONS TOWER (Animated Dish) */}
            <g transform="translate(420, 1020)">
              <line x1="-15" y1="0" x2="0" y2="-140" stroke={INK_CHARCOAL} strokeWidth="4.5" />
              <line x1="15" y1="0" x2="0" y2="-140" stroke={INK_CHARCOAL} strokeWidth="4.5" />
              <line x1="-10" y1="-50" x2="10" y2="-50" stroke={INK_CHARCOAL} strokeWidth="3" />
              <line x1="-6" y1="-100" x2="6" y2="-100" stroke={INK_CHARCOAL} strokeWidth="3" />

              {/* Rotating Parabolic Dish */}
              <g transform={`translate(0, -150) rotate(${Math.sin(frame * 0.04) * 20})`}>
                <path d="M -32 0 Q 0 -35 32 0 Z" fill="#FFFFFF" stroke={INK_CHARCOAL} strokeWidth="4" />
                <line x1="0" y1="-15" x2="0" y2="-35" stroke={INK_CHARCOAL} strokeWidth="3" />
                <circle cx="0" cy="-38" r="4" fill={WARM_GOLD} />
              </g>
            </g>

            {/* Foreground Dunes */}
            <path
              d="M -40 1220 Q 280 1160 580 1230 Q 860 1290 1120 1210 L 1120 1920 L -40 1920 Z"
              fill="url(#dunes-gradient)"
              stroke={INK_CHARCOAL}
              strokeWidth="9"
            />
          </g>
        )}

        {/* ========================================================================= */}
        {/* SCENE 5: VIOLENT GLOBAL DUST STORM (TEMPEST VISUALS - ZERO PPT BOXES)     */}
        {/* ========================================================================= */}
        {sceneId === 5 && (
          <g>
            {/* Blotted Out Dark Crimson Sky */}
            <rect width="1080" height="1920" fill="#5E271E" />
            <circle cx="340" cy="400" r="38" fill="#AA4E3A" stroke="#843424" strokeWidth="3" opacity="0.4" />

            {/* Violent High-Velocity Wind Streaks Across the Entire Screen */}
            <g stroke="#E8765A" strokeWidth="5" strokeLinecap="round" opacity="0.75">
              {[...Array(30)].map((_, i) => {
                const wx = ((stormWinds + i * 90) % 1600) - 300;
                const wy = 200 + (i * 48) + Math.sin(frame * 0.2 + i) * 25;
                const wlen = 180 + (i % 6) * 60;
                return (
                  <line key={i} x1={wx} y1={wy} x2={wx + wlen} y2={wy + 18} />
                );
              })}
            </g>

            {/* Swirling Giant Sand Devils */}
            <g transform={`translate(${720 - (frame * 5) % 400}, 920)`} opacity="0.6">
              <ellipse cx="0" cy="-220" rx="95" ry="26" fill="#AD4E38" stroke={INK_CHARCOAL} strokeWidth="4" />
              <ellipse cx="0" cy="-140" rx="65" ry="18" fill="#AD4E38" stroke={INK_CHARCOAL} strokeWidth="3.5" />
              <ellipse cx="0" cy="-60" rx="38" ry="12" fill="#AD4E38" stroke={INK_CHARCOAL} strokeWidth="3" />
              <ellipse cx="0" cy="20" rx="14" ry="6" fill="#AD4E38" stroke={INK_CHARCOAL} strokeWidth="2.5" />
            </g>

            {/* Base Alpha Covered in Dust with Red Emergency Strobe */}
            <g transform="translate(340, 1180)">
              <path d="M -180 0 A 180 180 0 0 1 180 0 Z" fill="#753528" stroke={INK_CHARCOAL} strokeWidth="6" />
              {/* Emergency Beacon Flashing Red */}
              <circle
                cx="0"
                cy="-185"
                r="12"
                fill={frame % 10 < 5 ? "#FF2A2A" : "#501212"}
                stroke={INK_CHARCOAL}
                strokeWidth="3.5"
              />
            </g>

            {/* Foreground Dunes Engulfed by Storm */}
            <path
              d="M -40 1200 Q 280 1140 580 1210 Q 860 1270 1120 1190 L 1120 1920 L -40 1920 Z"
              fill="#742A1D"
              stroke={INK_CHARCOAL}
              strokeWidth="9"
            />
          </g>
        )}

        {/* ========================================================================= */}
        {/* SCENE 6: MARS ASCENT VEHICLE ROCKET LAUNCH (TRIUMPHANT INTERPLANETARY)    */}
        {/* ========================================================================= */}
        {sceneId === 6 && (
          <g>
            <rect width="1080" height="1920" fill="url(#deep-space)" />

            {/* Distant Stars */}
            <g fill="#FFFFFF">
              {[
                [150, 120], [350, 90], [750, 140], [920, 100],
                [180, 320], [840, 280], [120, 520], [940, 480]
              ].map(([sx, sy], i) => (
                <circle key={i} cx={sx} cy={sy} r="2.5" opacity={starTwinkle} />
              ))}
            </g>

            {/* Curving Planet Horizon Below */}
            <ellipse cx="540" cy="1780" rx="720" ry="340" fill={DUSTY_CORAL} stroke={INK_CHARCOAL} strokeWidth="8" />

            {/* Tiny Base Alpha on Horizon Below */}
            <g transform="translate(320, 1520)">
              <ellipse cx="0" cy="0" rx="35" ry="18" fill="#EAE4D8" stroke={INK_CHARCOAL} strokeWidth="3" />
            </g>

            {/* Launch Pad Gantry left behind */}
            <g transform="translate(540, 1500)">
              <rect x="-35" y="-40" width="70" height="40" rx="4" fill="#525E70" stroke={INK_CHARCOAL} strokeWidth="4" />
              <line x1="-30" y1="-80" x2="-30" y2="0" stroke={INK_CHARCOAL} strokeWidth="4" />
              <line x1="30" y1="-80" x2="30" y2="0" stroke={INK_CHARCOAL} strokeWidth="4" />
            </g>

            {/* Billowing Giant Launch Exhaust Clouds */}
            <g fill="#EAE4D8" stroke={INK_CHARCOAL} strokeWidth="4" opacity="0.88">
              <ellipse cx="440" cy="1480" rx="110" ry="60" />
              <ellipse cx="640" cy="1475" rx="115" ry="62" />
              <ellipse cx="540" cy="1450" rx="140" ry="70" />
            </g>

            {/* =============================================================== */}
            {/* THE MARS ASCENT VEHICLE (MAV) ROCKET BLASTING INTO SPACE        */}
            {/* =============================================================== */}
            <g transform={`translate(540, ${1100 - rocketLift})`}>
              {/* Massive Thruster Exhaust Flame Plume */}
              <polygon
                points={`-35,160 0,${420 + flameFlicker} 35,160`}
                fill="url(#rocket-flame)"
              />
              <polygon
                points={`-18,160 0,${310 + flameFlicker} 18,160`}
                fill="#FFFFFF"
              />

              {/* Rocket Fuselage */}
              <rect x="-45" y="-140" width="90" height="290" rx="14" fill="#FFFFFF" stroke={INK_CHARCOAL} strokeWidth="7" />
              <path d="M -45 -140 Q 0 -240 45 -140 Z" fill="#EAE4D8" stroke={INK_CHARCOAL} strokeWidth="6" />
              <ellipse cx="0" cy="-100" rx="20" ry="12" fill={MUTED_BLUE} stroke={INK_CHARCOAL} strokeWidth="3.5" />

              <line x1="-45" y1="20" x2="45" y2="20" stroke={INK_CHARCOAL} strokeWidth="4" />
              <line x1="-45" y1="110" x2="45" y2="110" stroke={INK_CHARCOAL} strokeWidth="4" />

              {/* Delta Fins */}
              <polygon points="-45,70 -95,160 -45,150" fill={DUSTY_CORAL} stroke={INK_CHARCOAL} strokeWidth="5" />
              <polygon points="45,70 95,160 45,150" fill={DUSTY_CORAL} stroke={INK_CHARCOAL} strokeWidth="5" />

              {/* Engine Bells */}
              <polygon points="-28,150 -36,175 -8,175 -16,150" fill="#242B35" stroke={INK_CHARCOAL} strokeWidth="3" />
              <polygon points="16,150 8,175 36,175 28,150" fill="#242B35" stroke={INK_CHARCOAL} strokeWidth="3" />
            </g>

            {/* CLEAN CINEMATIC TITLE OVERLAY (NO BOXES, NO OVERFLOW) */}
            <g transform="translate(540, 240)">
              <text
                x="0"
                y="0"
                textAnchor="middle"
                fill="#FFFFFF"
                fontSize="50"
                fontWeight="900"
                letterSpacing="3px"
                fontFamily='"Montserrat", "Arial Black", sans-serif'
                stroke="#000000"
                strokeWidth="7"
                paintOrder="stroke fill"
              >
                30 DAYS ON MARS
              </text>
              <text
                x="0"
                y="65"
                textAnchor="middle"
                fill={WARM_GOLD}
                fontSize="26"
                fontWeight="800"
                letterSpacing="3px"
                fontFamily='"Montserrat", sans-serif'
                stroke="#000000"
                strokeWidth="5"
                paintOrder="stroke fill"
              >
                MISSION ACCOMPLISHED // INTERPLANETARY
              </text>
            </g>
          </g>
        )}
      </svg>
    </div>
  );
};
