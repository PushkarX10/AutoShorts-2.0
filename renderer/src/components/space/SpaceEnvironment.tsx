import React from "react";
import { useCurrentFrame } from "remotion";

interface SpaceEnvironmentProps {
  environment: string;
  planet?: "mars" | "moon" | "jupiter" | "venus" | "titan" | "deep_space";
  sceneId: number;
}

/**
 * Handcrafted 2D Space & Planetary Environment (v2.1)
 * Rich visual storytelling with distinct scenes and authentic assets:
 * - Scene 1: Planet Mars globe from space, burning Sun, orbiting science satellite & spacecraft
 * - Scene 2: 3-story exploration lander spacecraft on Martian dunes, parabolic low-g flight arc
 * - Scene 3: Mars scientific rover with robotic drill, Earth vs Mars atmospheric pressure infographic
 * - Scene 4: Base Alpha geodesic habitat dome, dual-axis solar panel farm, communications tower & docked rover
 * - Scene 5: Violent 100 km/h global dust storm, swirling sand devils, orbital weather satellite inset
 * - Scene 6: Mars Ascent Vehicle (MAV) rocket launch with roaring fire plume, exhaust clouds, mission success badge
 */
export const SpaceEnvironment: React.FC<SpaceEnvironmentProps> = ({
  environment,
  planet = "mars",
  sceneId,
}) => {
  const frame = useCurrentFrame();

  // Strict Handcrafted Editorial Palette
  const PAPER_CREAM = "#F4EFE5";
  const INK_CHARCOAL = "#242B35";
  const DUSTY_CORAL = "#C86D52";
  const MUTED_BLUE = "#527A9B";
  const WARM_GOLD = "#D5AA62";
  const STONE_GREY = "#A6A18F";
  const SAGE_GREEN = "#768C79";
  const SAND_BEIGE = "#D8C5AA";
  const SPACE_BLACK = "#0D1117";

  // Dynamic animations
  const starTwinkle = Math.sin(frame * 0.08) * 0.25 + 0.75;
  const sunPulse = Math.sin(frame * 0.04) * 4;
  const satelliteDrift = Math.sin(frame * 0.03) * 12;
  const roverArmMove = Math.sin(frame * 0.06) * 6;
  const dustDrift = (frame * 18) % 1400;
  const stormWinds = (frame * 36) % 1600;
  const rocketLift = Math.min(frame * 14, 550);
  const flameFlicker = (frame % 3) * 6;

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
          {/* Subtle paper grain */}
          <filter id="env-grain" x="0%" y="0%" width="100%" height="100%">
            <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="3" result="noise" />
            <feColorMatrix type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 0.05 0" />
            <feBlend mode="multiply" in="SourceGraphic" />
          </filter>

          {/* Deep Space Gradient */}
          <radialGradient id="deep-space" cx="50%" cy="40%" r="70%">
            <stop offset="0%" stopColor="#1E2633" />
            <stop offset="60%" stopColor="#121720" />
            <stop offset="100%" stopColor="#080B0F" />
          </radialGradient>

          {/* Mars Atmospheric Sky Gradient */}
          <linearGradient id="mars-sky" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#161C24" />
            <stop offset="40%" stopColor="#2A3340" />
            <stop offset="70%" stopColor="#5B4845" />
            <stop offset="100%" stopColor="#8C4E3D" />
          </linearGradient>

          {/* Mars Planet Sphere Gradient */}
          <radialGradient id="mars-globe" cx="35%" cy="35%" r="65%">
            <stop offset="0%" stopColor="#E27457" />
            <stop offset="50%" stopColor="#BD5338" />
            <stop offset="85%" stopColor="#7E2C1E" />
            <stop offset="100%" stopColor="#3A110B" />
          </radialGradient>

          {/* Sun Glow */}
          <radialGradient id="sun-corona" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#FFFFFF" stopOpacity="1" />
            <stop offset="30%" stopColor="#FFF2D1" stopOpacity="0.95" />
            <stop offset="60%" stopColor={WARM_GOLD} stopOpacity="0.6" />
            <stop offset="85%" stopColor={DUSTY_CORAL} stopOpacity="0.2" />
            <stop offset="100%" stopColor="transparent" stopOpacity="0" />
          </radialGradient>

          {/* Rocket Exhaust Plume */}
          <linearGradient id="rocket-flame" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#FFFFFF" />
            <stop offset="25%" stopColor="#FFF1B8" />
            <stop offset="60%" stopColor="#FF7A33" />
            <stop offset="90%" stopColor={DUSTY_CORAL} />
            <stop offset="100%" stopColor="transparent" />
          </linearGradient>

          {/* Solar Panel Texture */}
          <linearGradient id="solar-cell" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#2D4D6B" />
            <stop offset="100%" stopColor="#17283B" />
          </linearGradient>

          {/* Martian Dunes Gradient */}
          <linearGradient id="dunes-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor={DUSTY_CORAL} />
            <stop offset="50%" stopColor="#AD533B" />
            <stop offset="100%" stopColor="#6E2F20" />
          </linearGradient>
        </defs>

        {/* ========================================================================= */}
        {/* SCENE 1: ORBITAL ARRIVAL (PLANET MARS, SUN, SATELLITE & SPACECRAFT)      */}
        {/* ========================================================================= */}
        {sceneId === 1 && (
          <g>
            {/* Deep Starry Cosmos */}
            <rect width="1080" height="1920" fill="url(#deep-space)" />

            {/* Stars */}
            <g fill="#FFFFFF">
              {[
                [120, 180, 2], [280, 110, 1.5], [450, 240, 2.5], [780, 160, 2],
                [920, 290, 1.5], [140, 420, 2], [320, 580, 1.5], [90, 890, 2.5],
                [210, 1200, 1.5], [890, 1340, 2], [970, 950, 2.5], [840, 680, 1.5],
                [520, 1480, 2], [340, 1680, 1.5], [780, 1720, 2.5], [150, 1550, 2]
              ].map(([sx, sy, sr], i) => (
                <circle
                  key={i}
                  cx={sx}
                  cy={sy}
                  r={sr}
                  opacity={(i % 2 === 0 ? starTwinkle : 0.85)}
                />
              ))}
            </g>

            {/* THE SUN (Glowing Solar Corona in Deep Space) */}
            <g transform="translate(180, 280)">
              <circle cx="0" cy="0" r={160 + sunPulse} fill="url(#sun-corona)" />
              <circle cx="0" cy="0" r="54" fill="#FFFBE8" stroke={WARM_GOLD} strokeWidth="4" />
              {/* Sun Flare Rays */}
              {[0, 45, 90, 135, 180, 225, 270, 315].map((deg, idx) => (
                <line
                  key={idx}
                  x1="0"
                  y1="0"
                  x2={Math.cos((deg * Math.PI) / 180) * 90}
                  y2={Math.sin((deg * Math.PI) / 180) * 90}
                  stroke={WARM_GOLD}
                  strokeWidth="3"
                  strokeLinecap="round"
                  opacity="0.75"
                />
              ))}
            </g>

            {/* PLANET MARS GLOBE (Massive high-detail 2D illustrated sphere) */}
            <g transform="translate(680, 980)">
              {/* Atmospheric Limb Glow */}
              <circle cx="0" cy="0" r="375" fill="none" stroke="#6893B8" strokeWidth="12" opacity="0.6" />
              <circle cx="0" cy="0" r="370" fill="none" stroke={DUSTY_CORAL} strokeWidth="6" opacity="0.4" />

              {/* Main Planet Sphere */}
              <circle
                cx="0"
                cy="0"
                r="360"
                fill="url(#mars-globe)"
                stroke={INK_CHARCOAL}
                strokeWidth="7"
              />

              {/* North Polar Ice Cap (Planum Boreum) */}
              <path
                d="M -110 -310 Q 0 -360 110 -310 Q 60 -270 -30 -280 Q -90 -290 -110 -310 Z"
                fill="#F8F6F0"
                stroke={INK_CHARCOAL}
                strokeWidth="3.5"
              />

              {/* Valles Marineris Canyon & Dark Volcanic Regolith Basins */}
              <path
                d="M -160 -40 Q -40 20 140 -20 Q 220 10 260 -5 Q 210 25 130 15 Q -60 45 -160 -40 Z"
                fill="#541B13"
                stroke={INK_CHARCOAL}
                strokeWidth="4"
              />
              <path
                d="M -220 80 Q -140 140 -60 110 Q 20 170 -40 210 Q -180 230 -220 80 Z"
                fill="#4D1A13"
                stroke={INK_CHARCOAL}
                strokeWidth="3"
              />

              {/* Olympus Mons Volcano Shield Silhouette */}
              <ellipse cx="-130" cy="-140" rx="48" ry="32" fill="#782E20" stroke={INK_CHARCOAL} strokeWidth="3" />
              <ellipse cx="-130" cy="-140" rx="16" ry="10" fill="#441710" />
            </g>

            {/* ORBITING SCIENTIFIC SATELLITE (Detailed Telemetry Orbiter) */}
            <g transform={`translate(${280 + satelliteDrift}, ${1020 - satelliteDrift * 0.5})`}>
              {/* Satellite Body (Gold-foil bus) */}
              <rect x="-40" y="-35" width="80" height="70" rx="8" fill={WARM_GOLD} stroke={INK_CHARCOAL} strokeWidth="5" />
              <rect x="-30" y="-25" width="60" height="50" rx="4" fill="#B88A3B" />
              {/* Thermal radiator ribs */}
              <line x1="-30" y1="0" x2="30" y2="0" stroke={INK_CHARCOAL} strokeWidth="3" />

              {/* High-Gain Parabolic Dish Antenna */}
              <path d="M 0 -35 Q 25 -75 55 -60 Q 25 -45 0 -35 Z" fill="#E8E2D5" stroke={INK_CHARCOAL} strokeWidth="4" />
              <line x1="25" y1="-55" x2="42" y2="-75" stroke={INK_CHARCOAL} strokeWidth="3" />
              <circle cx="44" cy="-77" r="4" fill={DUSTY_CORAL} />

              {/* Left Solar Panel Wing */}
              <g transform="translate(-40, 0)">
                <line x1="0" y1="0" x2="-140" y2="0" stroke={INK_CHARCOAL} strokeWidth="6" />
                <rect x="-140" y="-45" width="130" height="90" rx="6" fill="url(#solar-cell)" stroke={INK_CHARCOAL} strokeWidth="4" />
                {/* Solar Cell Grid Lines */}
                <line x1="-97" y1="-45" x2="-97" y2="45" stroke="#4878A4" strokeWidth="2" />
                <line x1="-54" y1="-45" x2="-54" y2="45" stroke="#4878A4" strokeWidth="2" />
                <line x1="-140" y1="-15" x2="-10" y2="-15" stroke="#4878A4" strokeWidth="2" />
                <line x1="-140" y1="15" x2="-10" y2="15" stroke="#4878A4" strokeWidth="2" />
              </g>

              {/* Right Solar Panel Wing */}
              <g transform="translate(40, 0)">
                <line x1="0" y1="0" x2="140" y2="0" stroke={INK_CHARCOAL} strokeWidth="6" />
                <rect x="10" y="-45" width="130" height="90" rx="6" fill="url(#solar-cell)" stroke={INK_CHARCOAL} strokeWidth="4" />
                {/* Solar Cell Grid Lines */}
                <line x1="53" y1="-45" x2="53" y2="45" stroke="#4878A4" strokeWidth="2" />
                <line x1="96" y1="-45" x2="96" y2="45" stroke="#4878A4" strokeWidth="2" />
                <line x1="10" y1="-15" x2="140" y2="-15" stroke="#4878A4" strokeWidth="2" />
                <line x1="10" y1="15" x2="140" y2="15" stroke="#4878A4" strokeWidth="2" />
              </g>

              {/* Telemetry Boom */}
              <line x1="0" y1="35" x2="0" y2="90" stroke={INK_CHARCOAL} strokeWidth="4" />
              <circle cx="0" cy="94" r="6" fill={SAGE_GREEN} stroke={INK_CHARCOAL} strokeWidth="3" />
            </g>

            {/* INTERPLANETARY CRUISE SPACECRAFT (Cruising in high orbit) */}
            <g transform="translate(680, 460) scale(0.85)">
              {/* Fuselage */}
              <rect x="-80" y="-22" width="160" height="44" rx="14" fill="#EAE4D8" stroke={INK_CHARCOAL} strokeWidth="5" />
              {/* Cockpit Window Visor */}
              <path d="M 50 -12 Q 80 0 50 12 Z" fill={MUTED_BLUE} stroke={INK_CHARCOAL} strokeWidth="3.5" />
              {/* Main Thruster Bell */}
              <polygon points="-80,-18 -115,-30 -115,30 -80,18" fill="#5A6678" stroke={INK_CHARCOAL} strokeWidth="4" />
              {/* Thruster exhaust glow */}
              <ellipse cx="-120" cy="0" rx="15" ry="8" fill="#7FB7E0" opacity="0.8" />
              {/* Radiator Panels */}
              <rect x="-35" y="-55" width="70" height="30" rx="4" fill="#D5AA62" stroke={INK_CHARCOAL} strokeWidth="3" />
              <rect x="-35" y="25" width="70" height="30" rx="4" fill="#D5AA62" stroke={INK_CHARCOAL} strokeWidth="3" />
            </g>
          </g>
        )}

        {/* ========================================================================= */}
        {/* SCENE 2: SURFACE LANDER & LOW-G PHYSICS (TOUCHDOWN AT CHRYSE PLANITIA)    */}
        {/* ========================================================================= */}
        {sceneId === 2 && (
          <g>
            {/* Martian Sky */}
            <rect width="1080" height="1920" fill="url(#mars-sky)" />

            {/* Distant Sun & Phobos */}
            <circle cx="820" cy="380" r="42" fill="#FFE8BF" stroke={WARM_GOLD} strokeWidth="3" />
            {/* Phobos moon */}
            <ellipse cx="620" cy="290" rx="18" ry="12" fill="#A89F91" stroke={INK_CHARCOAL} strokeWidth="2.5" />

            {/* Distant Mountains & Olympus Mons Horizon */}
            <polygon
              points="-50,960 180,880 440,940 760,860 1130,930 1130,1300 -50,1300"
              fill="#522920"
              stroke={INK_CHARCOAL}
              strokeWidth="5"
            />

            {/* Midground Dunes */}
            <path
              d="M -40 1120 Q 280 1060 620 1130 Q 920 1180 1120 1100 L 1120 1450 L -40 1450 Z"
              fill="#853C2C"
              stroke={INK_CHARCOAL}
              strokeWidth="6"
            />

            {/* =============================================================== */}
            {/* 3-STORY EXPLORATION LANDER SPACECRAFT (Towers beside astronaut) */}
            {/* =============================================================== */}
            <g transform="translate(240, 1020)">
              {/* Lander Main Cylindrical Body */}
              <rect x="-85" y="-360" width="170" height="340" rx="20" fill="#EAE4D8" stroke={INK_CHARCOAL} strokeWidth="7" />
              {/* Nosecone Dome */}
              <path d="M -85 -360 Q 0 -440 85 -360 Z" fill="#D8D0C2" stroke={INK_CHARCOAL} strokeWidth="6" />

              {/* Heat Shield Base */}
              <rect x="-95" y="-20" width="190" height="24" rx="6" fill="#3D4552" stroke={INK_CHARCOAL} strokeWidth="5" />

              {/* Center Thruster Engine Bell */}
              <polygon points="-25,4 -45,45 45,45 25,4" fill="#242B35" stroke={INK_CHARCOAL} strokeWidth="4" />

              {/* Left Hydraulic Landing Leg */}
              <path d="M -85 -30 L -170 65 L -165 75 L -80 -10" fill="#525E70" stroke={INK_CHARCOAL} strokeWidth="5" />
              {/* Footpad */}
              <ellipse cx="-175" cy="72" rx="35" ry="12" fill="#343C47" stroke={INK_CHARCOAL} strokeWidth="4.5" />
              <line x1="-85" y1="-140" x2="-150" y2="40" stroke={INK_CHARCOAL} strokeWidth="4" />

              {/* Right Hydraulic Landing Leg */}
              <path d="M 85 -30 L 170 65 L 165 75 L 80 -10" fill="#525E70" stroke={INK_CHARCOAL} strokeWidth="5" />
              {/* Footpad */}
              <ellipse cx="175" cy="72" rx="35" ry="12" fill="#343C47" stroke={INK_CHARCOAL} strokeWidth="4.5" />
              <line x1="85" y1="-140" x2="150" y2="40" stroke={INK_CHARCOAL} strokeWidth="4" />

              {/* Crew Exit Airlock & Deployed Ladder */}
              <rect x="-26" y="-120" width="52" height="75" rx="8" fill="#2C3542" stroke={INK_CHARCOAL} strokeWidth="4" />
              {/* Ladder Rails */}
              <line x1="-16" y1="-45" x2="-16" y2="70" stroke={INK_CHARCOAL} strokeWidth="4" />
              <line x1="16" y1="-45" x2="16" y2="70" stroke={INK_CHARCOAL} strokeWidth="4" />
              {/* Ladder Rungs */}
              {[-30, -10, 10, 30, 50].map((ly, idx) => (
                <line key={idx} x1="-16" y1={ly} x2="16" y2={ly} stroke={INK_CHARCOAL} strokeWidth="3.5" />
              ))}

              {/* Mission Decal Flag */}
              <rect x="-55" y="-310" width="35" height="24" fill={WARM_GOLD} stroke={INK_CHARCOAL} strokeWidth="2.5" />
              <text x="25" y="-292" fill={INK_CHARCOAL} fontSize="17" fontWeight="900" fontFamily="sans-serif">
                ARES-IV
              </text>

              {/* Communication Dish Mast */}
              <line x1="0" y1="-430" x2="0" y2="-490" stroke={INK_CHARCOAL} strokeWidth="4.5" />
              <path d="M -22 -490 Q 0 -515 22 -490 Z" fill="#FFFFFF" stroke={INK_CHARCOAL} strokeWidth="3" />
            </g>

            {/* Parabolic Jump Trajectory Arc (Gold Dotted Physics) */}
            <path
              d="M 380 1240 Q 640 820 890 1240"
              fill="none"
              stroke={WARM_GOLD}
              strokeWidth="5"
              strokeDasharray="14 10"
            />
            {/* Velocity Vectors & Annotation */}
            <g transform="translate(640, 890)">
              <rect x="-125" y="-34" width="250" height="48" rx="10" fill={INK_CHARCOAL} stroke={WARM_GOLD} strokeWidth="2.5" />
              <text x="0" y="-3" textAnchor="middle" fill={WARM_GOLD} fontSize="19" fontWeight="900" fontFamily="sans-serif">
                GRAVITY: 0.38g (LOW-G)
              </text>
            </g>

            {/* Foreground Dunes */}
            <path
              d="M -40 1220 Q 280 1160 580 1230 Q 860 1290 1120 1210 L 1120 1920 L -40 1920 Z"
              fill="url(#dunes-gradient)"
              stroke={INK_CHARCOAL}
              strokeWidth="9"
            />

            {/* Regolith Rocks */}
            <g fill="#4A1E15" stroke={INK_CHARCOAL} strokeWidth="5" strokeLinejoin="round">
              <ellipse cx="490" cy="1260" rx="34" ry="16" />
              <ellipse cx="940" cy="1280" rx="44" ry="20" />
            </g>
          </g>
        )}

        {/* ========================================================================= */}
        {/* SCENE 3: PLANET SCIENCE ROVER & ATMOSPHERIC INFOGRAPHIC                   */}
        {/* ========================================================================= */}
        {sceneId === 3 && (
          <g>
            {/* Clean Science Journal Canvas */}
            <rect width="1080" height="1920" fill={PAPER_CREAM} />

            {/* Editorial Outer Border */}
            <rect x="40" y="80" width="1000" height="1260" rx="20" fill="none" stroke={INK_CHARCOAL} strokeWidth="4" />

            {/* Header Banner */}
            <g transform="translate(80, 120)">
              <rect x="0" y="0" width="920" height="65" rx="12" fill={INK_CHARCOAL} />
              <text x="460" y="42" textAnchor="middle" fill={PAPER_CREAM} fontSize="25" fontWeight="900" letterSpacing="3px" fontFamily="sans-serif">
                ATMOSPHERIC HAZARD // MARS VS EARTH
              </text>
            </g>

            {/* Infographic Comparison Columns */}
            {/* Column 1: EARTH */}
            <g transform="translate(80, 210)">
              <rect x="0" y="0" width="440" height="420" rx="14" fill="#E8E2D5" stroke={INK_CHARCOAL} strokeWidth="4" />
              <rect x="20" y="16" width="400" height="45" rx="8" fill={MUTED_BLUE} />
              <text x="220" y="47" textAnchor="middle" fill="#FFFFFF" fontSize="22" fontWeight="900" fontFamily="sans-serif">
                EARTH (HABITABLE)
              </text>
              <g transform="translate(25, 80)">
                <text x="0" y="30" fill={INK_CHARCOAL} fontSize="20" fontWeight="900" fontFamily="sans-serif">PRESSURE: 1013 hPa (1 ATM)</text>
                <text x="0" y="70" fill={INK_CHARCOAL} fontSize="20" fontWeight="900" fontFamily="sans-serif">OXYGEN: 21%</text>
                <text x="0" y="110" fill={INK_CHARCOAL} fontSize="20" fontWeight="900" fontFamily="sans-serif">CARBON DIOXIDE: 0.04%</text>
                <text x="0" y="150" fill={SAGE_GREEN} fontSize="20" fontWeight="900" fontFamily="sans-serif">STATUS: BREATHABLE OASIS</text>
              </g>
            </g>

            {/* Column 2: MARS */}
            <g transform="translate(560, 210)">
              <rect x="0" y="0" width="440" height="420" rx="14" fill="#F4DDD6" stroke={INK_CHARCOAL} strokeWidth="4" />
              <rect x="20" y="16" width="400" height="45" rx="8" fill={DUSTY_CORAL} />
              <text x="220" y="47" textAnchor="middle" fill="#FFFFFF" fontSize="22" fontWeight="900" fontFamily="sans-serif">
                MARS (LETHAL HAZARD)
              </text>
              <g transform="translate(25, 80)">
                <text x="0" y="30" fill={INK_CHARCOAL} fontSize="20" fontWeight="900" fontFamily="sans-serif">PRESSURE: 6 hPa (0.006 ATM)</text>
                <text x="0" y="70" fill={INK_CHARCOAL} fontSize="20" fontWeight="900" fontFamily="sans-serif">OXYGEN: 0.13%</text>
                <text x="0" y="110" fill={INK_CHARCOAL} fontSize="20" fontWeight="900" fontFamily="sans-serif">CARBON DIOXIDE: 95.3%</text>
                <text x="0" y="150" fill={DUSTY_CORAL} fontSize="20" fontWeight="900" fontFamily="sans-serif">STATUS: BLOOD BOILS IN 15s</text>
              </g>
            </g>

            {/* Armstrong Limit Warning Box */}
            <g transform="translate(80, 655)">
              <rect x="0" y="0" width="920" height="90" rx="14" fill={INK_CHARCOAL} stroke={DUSTY_CORAL} strokeWidth="3" />
              <polygon points="40,24 64,68 16,68" fill={DUSTY_CORAL} stroke={PAPER_CREAM} strokeWidth="2.5" />
              <text x="40" y="62" textAnchor="middle" fill={PAPER_CREAM} fontSize="24" fontWeight="900">!</text>
              <text x="80" y="42" fill={WARM_GOLD} fontSize="21" fontWeight="900" fontFamily="sans-serif">
                THE ARMSTRONG LIMIT (0.006 ATM):
              </text>
              <text x="80" y="68" fill={PAPER_CREAM} fontSize="18" fontWeight="700" fontFamily="sans-serif">
                At Mars pressure, water and body fluids vaporize at human body temperature (37°C).
              </text>
            </g>

            {/* =============================================================== */}
            {/* THE AUTONOMOUS MARS SCIENCE ROVER (Drilling bedrock in field)    */}
            {/* =============================================================== */}
            <g transform="translate(320, 1070)">
              {/* Rover Chassis */}
              <rect x="-110" y="-70" width="220" height="80" rx="16" fill="#DCD5C8" stroke={INK_CHARCOAL} strokeWidth="6" />
              <rect x="-85" y="-55" width="170" height="35" rx="8" fill="#525E70" />

              {/* Mast & Stereo Cameras */}
              <line x1="-60" y1="-70" x2="-60" y2="-170" stroke={INK_CHARCOAL} strokeWidth="6" strokeLinecap="round" />
              {/* Pan-Cam Head */}
              <rect x="-85" y="-200" width="50" height="32" rx="6" fill="#3D4552" stroke={INK_CHARCOAL} strokeWidth="4" />
              <circle cx="-72" cy="-184" r="7" fill={MUTED_BLUE} stroke={INK_CHARCOAL} strokeWidth="2.5" />
              <circle cx="-48" cy="-184" r="7" fill={MUTED_BLUE} stroke={INK_CHARCOAL} strokeWidth="2.5" />

              {/* High Gain Dish Antenna */}
              <line x1="50" y1="-70" x2="50" y2="-130" stroke={INK_CHARCOAL} strokeWidth="5" />
              <path d="M 30 -130 Q 50 -155 70 -130 Z" fill="#FFFFFF" stroke={INK_CHARCOAL} strokeWidth="3" />

              {/* Robotic Arm with Core Drill */}
              <g transform="translate(-110, -20)">
                <line x1="0" y1="0" x2={-60 - roverArmMove} y2="40" stroke={INK_CHARCOAL} strokeWidth="7" strokeLinecap="round" />
                <line x1={-60 - roverArmMove} y1="40" x2={-110 - roverArmMove} y2="85" stroke={INK_CHARCOAL} strokeWidth="6" strokeLinecap="round" />
                {/* Drill Head */}
                <rect x={-125 - roverArmMove} y="80" width="30" height="20" rx="4" fill="#6E7B8B" stroke={INK_CHARCOAL} strokeWidth="3" />
                <line x1={-110 - roverArmMove} y1="100" x2={-110 - roverArmMove} y2="125" stroke={WARM_GOLD} strokeWidth="4" />
              </g>

              {/* Rocker-Bogie Suspension & 6 Wheels */}
              {/* Bogie Struts */}
              <line x1="-80" y1="10" x2="-120" y2="70" stroke={INK_CHARCOAL} strokeWidth="6" />
              <line x1="0" y1="10" x2="0" y2="70" stroke={INK_CHARCOAL} strokeWidth="6" />
              <line x1="80" y1="10" x2="120" y2="70" stroke={INK_CHARCOAL} strokeWidth="6" />

              {/* 6 Cleated All-Terrain Wheels */}
              {[-120, 0, 120].map((wx, widx) => (
                <g key={widx} transform={`translate(${wx}, 85)`}>
                  <circle cx="0" cy="0" r="28" fill="#3D4552" stroke={INK_CHARCOAL} strokeWidth="5" />
                  <circle cx="0" cy="0" r="14" fill="#A89F91" stroke={INK_CHARCOAL} strokeWidth="3" />
                  {/* Wheel treads */}
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

              {/* Drilled Martian Bedrock Core */}
              <polygon points="-260,1180 -180,1130 -120,1190 -220,1230" fill="#8C3A29" stroke={INK_CHARCOAL} strokeWidth="4" />
            </g>
          </g>
        )}

        {/* ========================================================================= */}
        {/* SCENE 4: BASE ALPHA HABITAT, SOLAR FARM, COMMS TOWER & GREENHOUSE         */}
        {/* ========================================================================= */}
        {sceneId === 4 && (
          <g>
            {/* Martian Sky */}
            <rect width="1080" height="1920" fill="url(#mars-sky)" />

            {/* Sun */}
            <circle cx="280" cy="420" r="48" fill="#FFF2D6" stroke={WARM_GOLD} strokeWidth="4" />

            {/* Distant Hills */}
            <polygon
              points="-50,960 220,890 540,950 820,880 1130,940 1130,1350 -50,1350"
              fill="#522920"
              stroke={INK_CHARCOAL}
              strokeWidth="5"
            />

            {/* Midground Dunes */}
            <path
              d="M -40 1120 Q 280 1060 620 1130 Q 920 1180 1120 1100 L 1120 1450 L -40 1450 Z"
              fill="#853C2C"
              stroke={INK_CHARCOAL}
              strokeWidth="6"
            />

            {/* =============================================================== */}
            {/* BASE ALPHA GEODESIC DOME SANCTUARY                             */}
            {/* =============================================================== */}
            <g transform="translate(680, 1180)">
              {/* Geodesic Dome Outer Frame */}
              <path
                d="M -240 0 A 240 240 0 0 1 240 0 Z"
                fill="#EAE4D8"
                stroke={INK_CHARCOAL}
                strokeWidth="7"
              />

              {/* Interior Greenhouse Window Bay (Illuminated Hydroponic Plants) */}
              <path
                d="M -160 0 A 160 160 0 0 1 160 0 Z"
                fill="#D8E8D5"
                stroke={INK_CHARCOAL}
                strokeWidth="5"
              />
              {/* Hydroponic Plant Silhouettes inside Dome */}
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
                {/* Airlock Door */}
                <ellipse cx="-40" cy="-35" rx="24" ry="38" fill="#343C47" stroke={INK_CHARCOAL} strokeWidth="3.5" />
                {/* Status Indicator (Green Light: Pressurized) */}
                <circle cx="-40" cy="-65" r="5" fill="#3DDF78" stroke={INK_CHARCOAL} strokeWidth="2" />
              </g>
            </g>

            {/* DUAL-AXIS SOLAR COLLECTOR PANEL FARM (Left foreground) */}
            <g transform="translate(180, 1150)">
              {/* Solar Array 1 */}
              <g transform="translate(0, 0)">
                <line x1="0" y1="0" x2="0" y2="60" stroke={INK_CHARCOAL} strokeWidth="6" />
                <rect x="-65" y="-55" width="130" height="60" rx="6" fill="url(#solar-cell)" stroke={INK_CHARCOAL} strokeWidth="4.5" transform="rotate(-15)" />
              </g>
              {/* Solar Array 2 */}
              <g transform="translate(130, 20)">
                <line x1="0" y1="0" x2="0" y2="60" stroke={INK_CHARCOAL} strokeWidth="6" />
                <rect x="-65" y="-55" width="130" height="60" rx="6" fill="url(#solar-cell)" stroke={INK_CHARCOAL} strokeWidth="4.5" transform="rotate(-15)" />
              </g>
            </g>

            {/* COMMUNICATIONS DISH TOWER */}
            <g transform="translate(420, 1020)">
              {/* Steel Lattice Mast */}
              <line x1="-15" y1="0" x2="0" y2="-140" stroke={INK_CHARCOAL} strokeWidth="4.5" />
              <line x1="15" y1="0" x2="0" y2="-140" stroke={INK_CHARCOAL} strokeWidth="4.5" />
              <line x1="-10" y1="-50" x2="10" y2="-50" stroke={INK_CHARCOAL} strokeWidth="3" />
              <line x1="-6" y1="-100" x2="6" y2="-100" stroke={INK_CHARCOAL} strokeWidth="3" />
              {/* Parabolic Dish Antenna */}
              <path d="M -30 -140 Q 0 -175 30 -140 Z" fill="#FFFFFF" stroke={INK_CHARCOAL} strokeWidth="4" />
              <line x1="0" y1="-155" x2="0" y2="-175" stroke={INK_CHARCOAL} strokeWidth="3" />
              <circle cx="0" cy="-178" r="4" fill={WARM_GOLD} />
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
        {/* SCENE 5: GLOBAL DUST STORM & ORBITAL SATELLITE TRACKING                   */}
        {/* ========================================================================= */}
        {sceneId === 5 && (
          <g>
            {/* Storm Red Sky */}
            <rect width="1080" height="1920" fill="#5E271E" />

            {/* Blotted Out Dim Orange Sun */}
            <circle cx="340" cy="400" r="38" fill="#AA4E3A" stroke="#843424" strokeWidth="3" opacity="0.4" />

            {/* Violent Swirling Storm Front Particles & Wind Streaks */}
            <g stroke="#E8765A" strokeWidth="5" strokeLinecap="round" opacity="0.65">
              {[...Array(24)].map((_, i) => {
                const wx = ((stormWinds + i * 110) % 1500) - 200;
                const wy = 450 + (i * 45) + Math.sin(frame * 0.2 + i) * 20;
                const wlen = 160 + (i % 5) * 50;
                return (
                  <line key={i} x1={wx} y1={wy} x2={wx + wlen} y2={wy + 15} />
                );
              })}
            </g>

            {/* Swirling Mini Tornado / Dust Devil */}
            <g transform={`translate(${680 - (frame * 4) % 300}, 950)`} opacity="0.55">
              <ellipse cx="0" cy="-180" rx="80" ry="22" fill="#AD4E38" stroke={INK_CHARCOAL} strokeWidth="4" />
              <ellipse cx="0" cy="-110" rx="55" ry="16" fill="#AD4E38" stroke={INK_CHARCOAL} strokeWidth="3.5" />
              <ellipse cx="0" cy="-40" rx="30" ry="10" fill="#AD4E38" stroke={INK_CHARCOAL} strokeWidth="3" />
              <ellipse cx="0" cy="20" rx="12" ry="5" fill="#AD4E38" stroke={INK_CHARCOAL} strokeWidth="2.5" />
            </g>

            {/* Base Alpha Covered in Dust with Red Flashing Alarms */}
            <g transform="translate(340, 1180)">
              <path d="M -180 0 A 180 180 0 0 1 180 0 Z" fill="#753528" stroke={INK_CHARCOAL} strokeWidth="6" />
              {/* Emergency Beacon (Flashing Red) */}
              <circle
                cx="0"
                cy="-185"
                r="10"
                fill={frame % 12 < 6 ? "#FF2A2A" : "#601414"}
                stroke={INK_CHARCOAL}
                strokeWidth="3.5"
              />
            </g>

            {/* ORBITAL SATELLITE WEATHER TRACKING INSET (Upper Right Inset Monitor) */}
            <g transform="translate(620, 160)">
              {/* Monitor Frame */}
              <rect x="0" y="0" width="400" height="340" rx="14" fill={INK_CHARCOAL} stroke={PAPER_CREAM} strokeWidth="4" />
              {/* Monitor Screen */}
              <rect x="15" y="15" width="370" height="310" rx="8" fill="#131B26" />

              {/* Title Bar */}
              <text x="30" y="44" fill={WARM_GOLD} fontSize="17" fontWeight="900" fontFamily="sans-serif">
                ORBITAL TELEMETRY // SAT-09
              </text>
              <circle cx="360" cy="38" r="6" fill="#FF4545" />

              {/* Hemisphere Storm Map */}
              <circle cx="200" cy="180" r="100" fill="#BD5338" stroke="#FFFFFF" strokeWidth="2.5" />
              {/* Swirling Yellow Storm Vortex sweeping over globe */}
              <path
                d="M 120 160 Q 200 110 280 170 Q 260 250 160 230 Z"
                fill="#E8A34A"
                opacity="0.8"
                stroke="#FFFFFF"
                strokeWidth="2"
              />
              <text x="200" y="305" textAnchor="middle" fill="#FFFFFF" fontSize="15" fontWeight="900" fontFamily="monospace">
                STORM VELOCITY: 100 KM/H
              </text>
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
        {/* SCENE 6: MARS ASCENT VEHICLE ROCKET LAUNCH & MISSION COMPLETE FINALE      */}
        {/* ========================================================================= */}
        {sceneId === 6 && (
          <g>
            {/* Night Sky opening up as rocket ascends */}
            <rect width="1080" height="1920" fill="url(#deep-space)" />

            {/* Distant Stars */}
            <g fill="#FFFFFF">
              {[
                [150, 120], [350, 90], [750, 140], [920, 100],
                [180, 320], [840, 280], [120, 520], [940, 480]
              ].map(([sx, sy], i) => (
                <circle key={i} cx={sx} cy={sy} r="2" opacity={starTwinkle} />
              ))}
            </g>

            {/* Curving Martian Horizon Below */}
            <ellipse cx="540" cy="1780" rx="720" ry="340" fill={DUSTY_CORAL} stroke={INK_CHARCOAL} strokeWidth="8" />

            {/* Tiny Base Alpha on Horizon Below */}
            <g transform="translate(320, 1520)">
              <ellipse cx="0" cy="0" rx="35" ry="18" fill="#EAE4D8" stroke={INK_CHARCOAL} strokeWidth="3" />
            </g>

            {/* Launch Pad Gantry left behind on surface */}
            <g transform="translate(540, 1500)">
              <rect x="-35" y="-40" width="70" height="40" rx="4" fill="#525E70" stroke={INK_CHARCOAL} strokeWidth="4" />
              <line x1="-30" y1="-80" x2="-30" y2="0" stroke={INK_CHARCOAL} strokeWidth="4" />
              <line x1="30" y1="-80" x2="30" y2="0" stroke={INK_CHARCOAL} strokeWidth="4" />
            </g>

            {/* Billowing Exhaust Smoke Clouds on Launch Pad */}
            <g fill="#EAE4D8" stroke={INK_CHARCOAL} strokeWidth="4" opacity="0.85">
              <ellipse cx="460" cy="1480" rx="90" ry="50" />
              <ellipse cx="620" cy="1475" rx="95" ry="52" />
              <ellipse cx="540" cy="1460" rx="120" ry="60" />
            </g>

            {/* =============================================================== */}
            {/* THE MARS ASCENT VEHICLE (MAV) ROCKET BLASTING INTO SPACE        */}
            {/* =============================================================== */}
            <g transform={`translate(540, ${1100 - rocketLift})`}>
              {/* Roaring Rocket Fire Plume Exhaust */}
              <polygon
                points={`-35,160 0,${380 + flameFlicker} 35,160`}
                fill="url(#rocket-flame)"
              />
              <polygon
                points={`-18,160 0,${290 + flameFlicker} 18,160`}
                fill="#FFFFFF"
              />

              {/* Rocket Fuselage */}
              <rect x="-45" y="-140" width="90" height="290" rx="14" fill="#FFFFFF" stroke={INK_CHARCOAL} strokeWidth="7" />

              {/* Aerodynamic Nosecone */}
              <path d="M -45 -140 Q 0 -240 45 -140 Z" fill="#EAE4D8" stroke={INK_CHARCOAL} strokeWidth="6" />

              {/* Cockpit Visor Window */}
              <ellipse cx="0" cy="-100" rx="20" ry="12" fill={MUTED_BLUE} stroke={INK_CHARCOAL} strokeWidth="3.5" />

              {/* Staging Seams & Fin Fairings */}
              <line x1="-45" y1="20" x2="45" y2="20" stroke={INK_CHARCOAL} strokeWidth="4" />
              <line x1="-45" y1="110" x2="45" y2="110" stroke={INK_CHARCOAL} strokeWidth="4" />

              {/* Left Delta Fin */}
              <polygon points="-45,70 -95,160 -45,150" fill={DUSTY_CORAL} stroke={INK_CHARCOAL} strokeWidth="5" />
              {/* Right Delta Fin */}
              <polygon points="45,70 95,160 45,150" fill={DUSTY_CORAL} stroke={INK_CHARCOAL} strokeWidth="5" />

              {/* Rocket Engine Nozzle Bells */}
              <polygon points="-28,150 -36,175 -8,175 -16,150" fill="#242B35" stroke={INK_CHARCOAL} strokeWidth="3" />
              <polygon points="16,150 8,175 36,175 28,150" fill="#242B35" stroke={INK_CHARCOAL} strokeWidth="3" />
            </g>

            {/* TRIUMPHANT MISSION COMPLETE BADGE */}
            <g transform="translate(140, 240)">
              <rect x="0" y="0" width="800" height="150" rx="20" fill={INK_CHARCOAL} stroke={WARM_GOLD} strokeWidth="4" />
              <text x="400" y="60" textAnchor="middle" fill={WARM_GOLD} fontSize="34" fontWeight="900" letterSpacing="4px" fontFamily="sans-serif">
                30 DAYS ON MARS
              </text>
              <line x1="100" y1="85" x2="700" y2="85" stroke={STONE_GREY} strokeWidth="2" />
              <text x="400" y="122" textAnchor="middle" fill={PAPER_CREAM} fontSize="24" fontWeight="800" letterSpacing="2px" fontFamily="sans-serif">
                MISSION SUCCESSFUL // HUMANITY IS INTERPLANETARY
              </text>
            </g>
          </g>
        )}
      </svg>
    </div>
  );
};
