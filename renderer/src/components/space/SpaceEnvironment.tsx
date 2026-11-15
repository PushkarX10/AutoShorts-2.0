import React from "react";
import { useCurrentFrame } from "remotion";

interface SpaceEnvironmentProps {
  environment: string;
  planet?: "mars" | "moon" | "jupiter" | "venus" | "titan" | "deep_space";
  sceneId: number;
}

/**
 * Premium Handcrafted 2D Editorial Space Environment
 * Version 2.0 Aesthetic:
 * - Natural editorial science-journal illustration
 * - Organic, slightly hand-inked linework and etched terrain contours
 * - Authentic 9-color palette: Paper Cream, Ink Charcoal, Dusty Coral, Muted Blue, Warm Gold, Stone Grey, Sage Green, Sand Beige
 * - Textural depth, layered atmospheric plains, and custom architectural/scientific diagrams
 */
export const SpaceEnvironment: React.FC<SpaceEnvironmentProps> = ({
  environment,
  planet = "mars",
  sceneId,
}) => {
  const frame = useCurrentFrame();

  // Strict Version 2.0 Palette
  const PAPER_CREAM = "#F4EFE5";
  const INK_CHARCOAL = "#242B35";
  const DUSTY_CORAL = "#C86D52";
  const MUTED_BLUE = "#527A9B";
  const WARM_GOLD = "#D5AA62";
  const STONE_GREY = "#A6A18F";
  const SAGE_GREEN = "#768C79";
  const SAND_BEIGE = "#D8C5AA";
  const MUTED_BURGUNDY = "#8B5360";

  // Dynamic subtle motion
  const starTwinkle = Math.sin(frame * 0.08) * 0.25 + 0.75;
  const sunPulse = Math.sin(frame * 0.04) * 4;
  const dustDrift = (frame * 12) % 1200;
  const stormFront = (frame * 28) % 1400;

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        backgroundColor: INK_CHARCOAL,
        overflow: "hidden",
      }}
    >
      <svg
        viewBox="0 0 1080 1920"
        style={{ width: "100%", height: "100%" }}
        preserveAspectRatio="xMidYMid slice"
      >
        <defs>
          {/* Paper Texture Filter (Handcrafted Editorial Feel) */}
          <filter id="paper-grain" x="0%" y="0%" width="100%" height="100%">
            <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="3" result="noise" />
            <feColorMatrix
              type="matrix"
              values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 0.05 0"
            />
            <feBlend mode="multiply" in="SourceGraphic" />
          </filter>

          {/* Mars Atmospheric Sky Gradient: Deep Ink Zenith to Coral Horizon */}
          <linearGradient id="mars-sky" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#1A2028" />
            <stop offset="40%" stopColor="#2A3442" />
            <stop offset="70%" stopColor="#5B4845" />
            <stop offset="100%" stopColor="#8C4E3D" />
          </linearGradient>

          {/* Handcrafted Mars Dunes Gradient */}
          <linearGradient id="dunes-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor={DUSTY_CORAL} />
            <stop offset="50%" stopColor="#AD533B" />
            <stop offset="100%" stopColor="#6E2F20" />
          </linearGradient>

          {/* Distant Ridge Gradient */}
          <linearGradient id="mountains-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#5C3B34" />
            <stop offset="100%" stopColor="#2A1E20" />
          </linearGradient>

          {/* Warm Sun Corona */}
          <radialGradient id="sun-corona" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#FFFDF8" stopOpacity="1" />
            <stop offset="35%" stopColor={WARM_GOLD} stopOpacity="0.75" />
            <stop offset="70%" stopColor={DUSTY_CORAL} stopOpacity="0.25" />
            <stop offset="100%" stopColor="transparent" stopOpacity="0" />
          </radialGradient>

          {/* Geodesic Dome Warm Greenhouse Glow */}
          <radialGradient id="habitat-glow" cx="50%" cy="70%" r="60%">
            <stop offset="0%" stopColor={WARM_GOLD} stopOpacity="0.65" />
            <stop offset="45%" stopColor={SAGE_GREEN} stopOpacity="0.4" />
            <stop offset="100%" stopColor="#1E252F" stopOpacity="0.9" />
          </radialGradient>
        </defs>

        {/* ========================================================================= */}
        {/* SCENE 1 & 2: MARTIAN LANDSCAPE & LOW GRAVITY HORIZON                      */}
        {/* ========================================================================= */}
        {(environment === "mars_surface" || environment === "mars_arrival") && (
          <>
            {/* Sky */}
            <rect x="0" y="0" width="1080" height="1920" fill="url(#mars-sky)" />

            {/* Hand-drawn Soft Stars in Upper Atmosphere */}
            <g opacity={starTwinkle}>
              {[
                [110, 160, 2], [220, 85, 2.5], [380, 200, 1.8], [580, 130, 2],
                [820, 90, 3], [970, 210, 2], [80, 340, 1.8], [310, 420, 2.2],
                [730, 380, 2], [940, 460, 2.5], [510, 280, 2.8], [170, 540, 2],
              ].map(([sx, sy, sr], i) => (
                <circle key={i} cx={sx} cy={sy} r={sr} fill={PAPER_CREAM} />
              ))}
            </g>

            {/* Distant Sun (Appears smaller on Mars: 68% size of Earth Sun) */}
            <g transform="translate(840, 240)">
              <circle cx="0" cy="0" r={45 + sunPulse} fill="url(#sun-corona)" />
              <circle cx="0" cy="0" r="14" fill={PAPER_CREAM} stroke={WARM_GOLD} strokeWidth="3" />
            </g>

            {/* Handcrafted Phobos Moon (Potato Silhouette with Impact Crater) */}
            <g transform="translate(230, 300) rotate(-20)">
              <ellipse cx="0" cy="0" rx="20" ry="14" fill={STONE_GREY} stroke={INK_CHARCOAL} strokeWidth="3.5" />
              <circle cx="-5" cy="-2" r="4" fill="#8C8775" />
              <circle cx="7" cy="4" r="3" fill="#8C8775" />
              <circle cx="-1" cy="6" r="2" fill="#8C8775" />
            </g>

            {/* Distant Olympus Mons Silhouette with Hand-drawn Topo Lines */}
            <path
              d="M -40 920 Q 260 810 540 790 Q 820 810 1120 920 L 1120 1300 L -40 1300 Z"
              fill="url(#mountains-gradient)"
              stroke={INK_CHARCOAL}
              strokeWidth="5"
            />
            {/* Mountain Ridgeline Contours */}
            <path d="M 120 880 Q 320 840 540 830 Q 760 840 960 880" fill="none" stroke="#6E443B" strokeWidth="2.5" />
            <path d="M 280 845 Q 540 820 800 845" fill="none" stroke="#6E443B" strokeWidth="2" strokeDasharray="6 4" />

            {/* Midground Layer: Rocky Crags & Crater Ridges */}
            <polygon
              points="-40,1110 160,1035 340,1085 610,1015 860,1075 1120,1025 1120,1400 -40,1400"
              fill="#7A392B"
              stroke={INK_CHARCOAL}
              strokeWidth="6"
            />
            {/* Crater Rim in Midground */}
            <ellipse cx="440" cy="1065" rx="90" ry="18" fill="#5E2A1E" stroke={INK_CHARCOAL} strokeWidth="3.5" />
            <ellipse cx="440" cy="1065" rx="75" ry="12" fill="#4A1E14" />

            {/* =================================================================== */}
            {/* SCENE 2 SPECIFIC: LOW GRAVITY PHYSICS DIAGRAM OVERLAY              */}
            {/* =================================================================== */}
            {sceneId === 2 && (
              <g transform="translate(0, 0)">
                {/* Parabolic Jump Trajectory (Gold Dotted Arc) */}
                <path
                  d="M 220 1280 Q 480 820 740 1280"
                  fill="none"
                  stroke={WARM_GOLD}
                  strokeWidth="6"
                  strokeDasharray="14 10"
                />

                {/* Takeoff Launch Rings on Dune */}
                <ellipse cx="220" cy="1280" rx="35" ry="12" fill="none" stroke={WARM_GOLD} strokeWidth="3.5" />
                <ellipse cx="220" cy="1280" rx="20" ry="7" fill="none" stroke={WARM_GOLD} strokeWidth="2.5" opacity="0.6" />

                {/* Velocity Vector Arrow at Launch */}
                <line x1="220" y1="1280" x2="280" y2="1160" stroke={DUSTY_CORAL} strokeWidth="4" />
                <polygon points="280,1160 268,1176 288,1172" fill={DUSTY_CORAL} />
                <text x="300" y="1180" fill={PAPER_CREAM} fontSize="20" fontWeight="800" fontFamily="monospace">v₀ = 4.2 m/s</text>

                {/* Apex Annotation Tag */}
                <g transform="translate(480, 880)">
                  <rect x="-140" y="-35" width="280" height="48" rx="10" fill={INK_CHARCOAL} stroke={WARM_GOLD} strokeWidth="3" />
                  <text x="0" y="-3" textAnchor="middle" fill={WARM_GOLD} fontSize="20" fontWeight="900" fontFamily="sans-serif">
                    GRAVITY: 0.38g (BOUYANT)
                  </text>
                  <line x1="0" y1="13" x2="0" y2="35" stroke={WARM_GOLD} strokeWidth="3" />
                  <polygon points="0,35 -5,25 5,25" fill={WARM_GOLD} />
                </g>
              </g>
            )}

            {/* Foreground Mars Red Sand Dunes (Textured Layer) */}
            <path
              d="M -40 1250 Q 260 1195 540 1260 Q 820 1315 1120 1245 L 1120 1920 L -40 1920 Z"
              fill="url(#dunes-gradient)"
              stroke={INK_CHARCOAL}
              strokeWidth="9"
            />

            {/* Dune Ridge Shading (Cross-hatched organic strokes) */}
            <g stroke="#91412E" strokeWidth="3" strokeLinecap="round">
              {[...Array(12)].map((_, i) => (
                <line
                  key={i}
                  x1={120 + i * 75}
                  y1={1240 + (i % 3) * 12}
                  x2={100 + i * 75}
                  y2={1275 + (i % 3) * 12}
                />
              ))}
            </g>

            {/* Hand-drawn Martian Boulders & Regolith Rocks */}
            <g fill="#4A1E15" stroke={INK_CHARCOAL} strokeWidth="5" strokeLinejoin="round">
              <ellipse cx="140" cy="1280" rx="36" ry="18" />
              <ellipse cx="880" cy="1290" rx="46" ry="22" />
              <ellipse cx="680" cy="1315" rx="24" ry="12" />
              <ellipse cx="380" cy="1330" rx="18" ry="9" />
            </g>

            {/* Swirling Martian Dust Devil Particles */}
            <g opacity="0.5">
              {[...Array(14)].map((_, i) => {
                const px = ((dustDrift + i * 90) % 1150) - 50;
                const py = 1200 + Math.sin(frame * 0.1 + i) * 30 + (i % 4) * 25;
                return (
                  <ellipse key={i} cx={px} cy={py} rx={14 + i * 2} ry="4" fill={SAND_BEIGE} />
                );
              })}
            </g>
          </>
        )}

        {/* ========================================================================= */}
        {/* SCENE 3: EDITORIAL SCIENCE JOURNAL SPREAD (EARTH VS MARS COMPARISON)     */}
        {/* ========================================================================= */}
        {environment === "planet_comparison" && (
          <>
            {/* Authentic Paper Cream Journal Background */}
            <rect x="0" y="0" width="1080" height="1920" fill={PAPER_CREAM} />

            {/* Subtle Journal Outer Margin Inset */}
            <rect x="40" y="240" width="1000" height="1140" rx="18" fill="none" stroke={INK_CHARCOAL} strokeWidth="4" />
            <rect x="48" y="248" width="984" height="1124" rx="14" fill="none" stroke={STONE_GREY} strokeWidth="1.5" />

            {/* Editorial Title Banner Plate */}
            <g transform="translate(100, 275)">
              <rect x="0" y="0" width="880" height="70" rx="12" fill={INK_CHARCOAL} />
              <text x="440" y="44" textAnchor="middle" fill={PAPER_CREAM} fontSize="26" fontWeight="900" letterSpacing="4px" fontFamily="'Outfit', sans-serif">
                COMPARATIVE PLANETARY TELEMETRY
              </text>
            </g>

            {/* Left Editorial Card: PLANET EARTH (Oasis) */}
            <g transform="translate(70, 375)">
              <rect x="0" y="0" width="450" height="780" rx="18" fill="#EAE4D8" stroke={INK_CHARCOAL} strokeWidth="5" />
              <rect x="25" y="22" width="400" height="55" rx="8" fill={MUTED_BLUE} />
              <text x="225" y="58" textAnchor="middle" fill={PAPER_CREAM} fontSize="24" fontWeight="900" fontFamily="sans-serif">
                EARTH (HOME OASIS)
              </text>

              {/* Handcrafted 2D Illustrated Earth */}
              <g transform="translate(225, 205)">
                {/* Ocean Sphere */}
                <circle cx="0" cy="0" r="95" fill={MUTED_BLUE} stroke={INK_CHARCOAL} strokeWidth="5" />
                {/* Sage Green Continents */}
                <path d="M -45 -35 Q -15 -75 35 -45 Q 60 -5 20 20 Q -35 55 -45 -35 Z" fill={SAGE_GREEN} stroke={INK_CHARCOAL} strokeWidth="2.5" />
                <path d="M 15 25 Q 55 35 35 75 Q -5 65 15 25 Z" fill={SAGE_GREEN} stroke={INK_CHARCOAL} strokeWidth="2.5" />
                {/* Polar Ice Cap */}
                <ellipse cx="0" cy="-85" rx="35" ry="10" fill={PAPER_CREAM} />
                {/* Atmospheric Corona */}
                <circle cx="0" cy="0" r="102" fill="none" stroke="#7FA3C2" strokeWidth="4" opacity="0.7" />
              </g>

              {/* Metric Data Rows */}
              <g transform="translate(35, 360)">
                <g transform="translate(0, 0)">
                  <rect x="0" y="0" width="380" height="48" rx="8" fill={PAPER_CREAM} stroke={STONE_GREY} strokeWidth="2" />
                  <text x="18" y="32" fill={INK_CHARCOAL} fontSize="20" fontWeight="900" fontFamily="sans-serif">GRAVITY</text>
                  <text x="360" y="32" textAnchor="end" fill={MUTED_BLUE} fontSize="20" fontWeight="900" fontFamily="monospace">1.0g (100%)</text>
                </g>
                <g transform="translate(0, 60)">
                  <rect x="0" y="0" width="380" height="48" rx="8" fill={PAPER_CREAM} stroke={STONE_GREY} strokeWidth="2" />
                  <text x="18" y="32" fill={INK_CHARCOAL} fontSize="20" fontWeight="900" fontFamily="sans-serif">PRESSURE</text>
                  <text x="360" y="32" textAnchor="end" fill={INK_CHARCOAL} fontSize="20" fontWeight="900" fontFamily="monospace">1.0 ATM</text>
                </g>
                <g transform="translate(0, 120)">
                  <rect x="0" y="0" width="380" height="48" rx="8" fill={PAPER_CREAM} stroke={STONE_GREY} strokeWidth="2" />
                  <text x="18" y="32" fill={INK_CHARCOAL} fontSize="20" fontWeight="900" fontFamily="sans-serif">ATMOSPHERE</text>
                  <text x="360" y="32" textAnchor="end" fill={SAGE_GREEN} fontSize="19" fontWeight="900" fontFamily="monospace">21% OXYGEN</text>
                </g>
                <g transform="translate(0, 180)">
                  <rect x="0" y="0" width="380" height="48" rx="8" fill={PAPER_CREAM} stroke={STONE_GREY} strokeWidth="2" />
                  <text x="18" y="32" fill={INK_CHARCOAL} fontSize="20" fontWeight="900" fontFamily="sans-serif">AVG TEMP</text>
                  <text x="360" y="32" textAnchor="end" fill={WARM_GOLD} fontSize="20" fontWeight="900" fontFamily="monospace">+15°C</text>
                </g>
                <g transform="translate(0, 240)">
                  <rect x="0" y="0" width="380" height="48" rx="8" fill={PAPER_CREAM} stroke={STONE_GREY} strokeWidth="2" />
                  <text x="18" y="32" fill={INK_CHARCOAL} fontSize="20" fontWeight="900" fontFamily="sans-serif">SURVIVAL</text>
                  <text x="360" y="32" textAnchor="end" fill={SAGE_GREEN} fontSize="18" fontWeight="900" fontFamily="monospace">HABITABLE</text>
                </g>
              </g>
            </g>

            {/* Right Editorial Card: PLANET MARS (Wasteland) */}
            <g transform="translate(560, 375)">
              <rect x="0" y="0" width="450" height="780" rx="18" fill="#EAE4D8" stroke={INK_CHARCOAL} strokeWidth="5" />
              <rect x="25" y="22" width="400" height="55" rx="8" fill={DUSTY_CORAL} />
              <text x="225" y="58" textAnchor="middle" fill={PAPER_CREAM} fontSize="24" fontWeight="900" fontFamily="sans-serif">
                MARS (SOL 18)
              </text>

              {/* Handcrafted 2D Illustrated Mars (53% of Earth diameter) */}
              <g transform="translate(225, 205)">
                <circle cx="0" cy="0" r="58" fill={DUSTY_CORAL} stroke={INK_CHARCOAL} strokeWidth="5" />
                {/* Iron oxide maria markings */}
                <ellipse cx="-12" cy="-8" rx="22" ry="12" fill="#8C3D2B" />
                <ellipse cx="18" cy="15" rx="18" ry="9" fill="#8C3D2B" />
                {/* White Dry Ice Polar Cap */}
                <ellipse cx="0" cy="-52" rx="20" ry="6" fill={PAPER_CREAM} />
              </g>

              {/* Metric Data Rows */}
              <g transform="translate(35, 360)">
                <g transform="translate(0, 0)">
                  <rect x="0" y="0" width="380" height="48" rx="8" fill={PAPER_CREAM} stroke={STONE_GREY} strokeWidth="2" />
                  <text x="18" y="32" fill={INK_CHARCOAL} fontSize="20" fontWeight="900" fontFamily="sans-serif">GRAVITY</text>
                  <text x="360" y="32" textAnchor="end" fill={DUSTY_CORAL} fontSize="20" fontWeight="900" fontFamily="monospace">0.38g (38%)</text>
                </g>
                <g transform="translate(0, 60)">
                  <rect x="0" y="0" width="380" height="48" rx="8" fill={PAPER_CREAM} stroke={STONE_GREY} strokeWidth="2" />
                  <text x="18" y="32" fill={INK_CHARCOAL} fontSize="20" fontWeight="900" fontFamily="sans-serif">PRESSURE</text>
                  <text x="360" y="32" textAnchor="end" fill={MUTED_BURGUNDY} fontSize="20" fontWeight="900" fontFamily="monospace">0.006 ATM</text>
                </g>
                <g transform="translate(0, 120)">
                  <rect x="0" y="0" width="380" height="48" rx="8" fill={PAPER_CREAM} stroke={STONE_GREY} strokeWidth="2" />
                  <text x="18" y="32" fill={INK_CHARCOAL} fontSize="20" fontWeight="900" fontFamily="sans-serif">ATMOSPHERE</text>
                  <text x="360" y="32" textAnchor="end" fill={MUTED_BURGUNDY} fontSize="19" fontWeight="900" fontFamily="monospace">95% CO2 (LETHAL)</text>
                </g>
                <g transform="translate(0, 180)">
                  <rect x="0" y="0" width="380" height="48" rx="8" fill={PAPER_CREAM} stroke={STONE_GREY} strokeWidth="2" />
                  <text x="18" y="32" fill={INK_CHARCOAL} fontSize="20" fontWeight="900" fontFamily="sans-serif">AVG TEMP</text>
                  <text x="360" y="32" textAnchor="end" fill={MUTED_BLUE} fontSize="20" fontWeight="900" fontFamily="monospace">-63°C</text>
                </g>
                <g transform="translate(0, 240)">
                  <rect x="0" y="0" width="380" height="48" rx="8" fill={PAPER_CREAM} stroke={STONE_GREY} strokeWidth="2" />
                  <text x="18" y="32" fill={INK_CHARCOAL} fontSize="20" fontWeight="900" fontFamily="sans-serif">SURVIVAL</text>
                  <text x="360" y="32" textAnchor="end" fill={MUTED_BURGUNDY} fontSize="18" fontWeight="900" fontFamily="monospace">&lt; 15 SECONDS</text>
                </g>
              </g>
            </g>

            {/* Bottom Scientific Insight Callout Plate: THE ARMSTRONG LIMIT */}
            <g transform="translate(70, 1195)">
              <rect x="0" y="0" width="940" height="95" rx="14" fill={INK_CHARCOAL} />
              <text x="470" y="40" textAnchor="middle" fill={WARM_GOLD} fontSize="22" fontWeight="900" letterSpacing="2px" fontFamily="monospace">
                ! THE ARMSTRONG LIMIT HAZARD !
              </text>
              <text x="470" y="74" textAnchor="middle" fill={PAPER_CREAM} fontSize="18" fontWeight="800" fontFamily="sans-serif">
                At 0.006 ATM, unprotected human blood boils at body temperature in 15 seconds.
              </text>
            </g>
          </>
        )}

        {/* ========================================================================= */}
        {/* SCENE 4: BASE ALPHA GEODESIC HABITAT & SOLAR ARRAYS                      */}
        {/* ========================================================================= */}
        {environment === "mars_habitat" && (
          <>
            {/* Dusk Martian Sky */}
            <rect x="0" y="0" width="1080" height="1920" fill="url(#mars-sky)" />

            {/* Distant Ridge */}
            <path d="M -40 1020 Q 300 920 600 960 Q 900 920 1120 1000 L 1120 1350 L -40 1350 Z" fill="#5C2D22" stroke={INK_CHARCOAL} strokeWidth="6" />

            {/* Pressurized Geodesic Habitat Dome (Architectural Cross-Section) */}
            <g transform="translate(540, 1260)">
              {/* Outer Protective Dome Shell */}
              <path
                d="M -340 0 C -340 -260, 340 -260, 340 0 Z"
                fill="#202A38"
                stroke={INK_CHARCOAL}
                strokeWidth="9"
              />
              {/* Warm Greenhouse Interior Glow */}
              <path d="M -330 -4 C -330 -250, 330 -250, 330 -4 Z" fill="url(#habitat-glow)" />

              {/* Hand-drawn Geodesic Hexagonal Lattice Struts */}
              <g stroke={PAPER_CREAM} strokeWidth="3" opacity="0.65">
                <line x1="-240" y1="-80" x2="-140" y2="-180" />
                <line x1="-140" y1="-180" x2="0" y2="-230" />
                <line x1="0" y1="-230" x2="140" y2="-180" />
                <line x1="140" y1="-180" x2="240" y2="-80" />
                <line x1="-240" y1="-80" x2="-140" y2="0" />
                <line x1="-140" y1="0" x2="0" y2="-100" />
                <line x1="0" y1="-100" x2="140" y2="0" />
                <line x1="140" y1="0" x2="240" y2="-80" />
                <line x1="-140" y1="-180" x2="-140" y2="0" />
                <line x1="140" y1="-180" x2="140" y2="0" />
              </g>

              {/* Interior Hydroponic Botanical Silhouettes */}
              <g fill={SAGE_GREEN} opacity="0.85">
                <ellipse cx="-180" cy="-25" rx="20" ry="40" />
                <ellipse cx="-205" cy="-20" rx="15" ry="30" />
                <ellipse cx="180" cy="-25" rx="20" ry="40" />
                <ellipse cx="205" cy="-20" rx="15" ry="30" />
              </g>

              {/* Illustrated Airlock Module 01 */}
              <rect x="-70" y="-130" width="140" height="130" rx="14" fill={PAPER_CREAM} stroke={INK_CHARCOAL} strokeWidth="6" />
              {/* Circular Sub-Door Hatch */}
              <circle cx="0" cy="-65" r="32" fill="#EAE4D8" stroke={INK_CHARCOAL} strokeWidth="4" />
              {/* Warm Hatch Window */}
              <circle cx="0" cy="-65" r="16" fill={WARM_GOLD} />
              <line x1="0" y1="-80" x2="0" y2="-50" stroke={INK_CHARCOAL} strokeWidth="3" />
              <line x1="-15" y1="-65" x2="15" y2="-65" stroke={INK_CHARCOAL} strokeWidth="3" />
              <text x="0" y="-15" textAnchor="middle" fill={INK_CHARCOAL} fontSize="14" fontWeight="900" fontFamily="monospace">AIRLOCK 01</text>
            </g>

            {/* Hand-drawn Solar Panel Bank */}
            <g transform="translate(60, 1160)" fill="#2C3D52" stroke={INK_CHARCOAL} strokeWidth="5">
              <polygon points="0,80 180,35 245,90 65,135" />
              {/* Grid cell lines */}
              <line x1="45" y1="68" x2="110" y2="122" stroke={WARM_GOLD} strokeWidth="2.5" />
              <line x1="90" y1="56" x2="155" y2="110" stroke={WARM_GOLD} strokeWidth="2.5" />
              <line x1="135" y1="44" x2="200" y2="98" stroke={WARM_GOLD} strokeWidth="2.5" />
              <line x1="120" y1="90" x2="120" y2="150" stroke={INK_CHARCOAL} strokeWidth="8" />
            </g>

            {/* Ground Dunes */}
            <polygon points="-40,1260 1120,1260 1120,1920 -40,1920" fill="url(#dunes-gradient)" />
            <line x1="-40" y1="1260" x2="1120" y2="1260" stroke={INK_CHARCOAL} strokeWidth="9" />
          </>
        )}

        {/* ========================================================================= */}
        {/* SCENE 5: SOL 18 DUST STORM CRISIS (85% POWER LOSS)                       */}
        {/* ========================================================================= */}
        {environment === "mars_dust_storm" && (
          <>
            {/* Blotted Out Dark Sky */}
            <rect x="0" y="0" width="1080" height="1920" fill="#241B1A" />

            {/* Giant Swirling Sandstorm Cloud Fronts */}
            <g opacity="0.85">
              <path
                d="M -50 250 Q 240 180 540 300 Q 840 160 1130 270 L 1130 1400 L -50 1400 Z"
                fill="#662920"
              />
              <path
                d="M -50 480 Q 300 400 600 500 Q 900 430 1130 520 L 1130 1400 L -50 1400 Z"
                fill="#8C3E30"
              />
              <path
                d="M -50 720 Q 250 640 550 740 Q 850 670 1130 760 L 1130 1400 L -50 1400 Z"
                fill="#B85942"
              />
            </g>

            {/* Rapid Horizontal 100 km/h Wind Motion Streaks */}
            <g stroke={SAND_BEIGE} opacity="0.75" strokeLinecap="round">
              {[...Array(28)].map((_, i) => {
                const wx = ((stormFront + i * 85) % 1500) - 300;
                const wy = 350 + ((i * 50) % 950);
                const wLen = 160 + (i % 6) * 45;
                return (
                  <line
                    key={i}
                    x1={wx}
                    y1={wy}
                    x2={wx + wLen}
                    y2={wy + 18}
                    strokeWidth={3 + (i % 3)}
                  />
                );
              })}
            </g>

            {/* Failing Solar Panels Blanketed in Sand */}
            <g transform="translate(180, 1160)" fill="#4A251C" stroke={INK_CHARCOAL} strokeWidth="5">
              <polygon points="0,75 180,32 240,82 60,125" />
              {/* Thick dusty coral sand drifts covering the panel */}
              <polygon points="12,72 175,34 230,80 55,120" fill={DUSTY_CORAL} opacity="0.9" />
              {/* Emergency Alert Tag Banner */}
              <g transform="translate(120, 10)">
                <rect x="-85" y="-18" width="170" height="36" rx="8" fill={MUTED_BURGUNDY} stroke={PAPER_CREAM} strokeWidth="2.5" />
                <text x="0" y="6" textAnchor="middle" fill={PAPER_CREAM} fontSize="16" fontWeight="900" fontFamily="sans-serif">
                  POWER LOSS: -85%
                </text>
              </g>
            </g>

            {/* Ground Dunes */}
            <polygon points="-40,1260 1120,1260 1120,1920 -40,1920" fill="#3D1812" />
            <line x1="-40" y1="1260" x2="1120" y2="1260" stroke={INK_CHARCOAL} strokeWidth="9" />
          </>
        )}

        {/* ========================================================================= */}
        {/* SCENE 6: INTERACTIVE SURVIVAL PROTOCOL CLIFFHANGER (A vs B)              */}
        {/* ========================================================================= */}
        {environment === "space_cliffhanger" && (
          <>
            {/* Paper Cream Editorial Background */}
            <rect x="0" y="0" width="1080" height="1920" fill={PAPER_CREAM} />

            {/* Inset Double Border */}
            <rect x="35" y="240" width="1010" height="1140" rx="18" fill="none" stroke={INK_CHARCOAL} strokeWidth="4.5" />
            <rect x="43" y="248" width="994" height="1124" rx="14" fill="none" stroke={STONE_GREY} strokeWidth="1.5" />

            {/* Main Decision Header Banner */}
            <g transform="translate(65, 275)">
              <rect x="0" y="0" width="950" height="75" rx="14" fill={INK_CHARCOAL} />
              <text x="475" y="48" textAnchor="middle" fill={PAPER_CREAM} fontSize="28" fontWeight="900" letterSpacing="3px" fontFamily="'Outfit', sans-serif">
                WHAT WOULD YOU DO TO SURVIVE?
              </text>
            </g>

            {/* Protocol [ A ]: BRAVE THE STORM */}
            <g transform="translate(65, 380)">
              <rect
                x="0"
                y="0"
                width="460"
                height="560"
                rx="18"
                fill="#EAE4D8"
                stroke={DUSTY_CORAL}
                strokeWidth="6"
              />
              <rect x="22" y="22" width="416" height="60" rx="10" fill={DUSTY_CORAL} />
              <text x="230" y="62" textAnchor="middle" fill={PAPER_CREAM} fontSize="24" fontWeight="900" fontFamily="sans-serif">
                [ A ] BRAVE THE STORM
              </text>

              {/* Handcrafted Tool / Panel Sweep Illustration */}
              <g transform="translate(145, 120)">
                <rect x="0" y="0" width="170" height="110" rx="12" fill={PAPER_CREAM} stroke={INK_CHARCOAL} strokeWidth="4" />
                <polygon points="20,80 150,40 150,70 20,95" fill={DUSTY_CORAL} opacity="0.4" />
                <line x1="85" y1="20" x2="85" y2="85" stroke={INK_CHARCOAL} strokeWidth="5" strokeLinecap="round" />
                <line x1="60" y1="85" x2="110" y2="85" stroke={WARM_GOLD} strokeWidth="6" strokeLinecap="round" />
              </g>

              {/* Outcome Telemetry Rows */}
              <g transform="translate(30, 265)">
                <g transform="translate(0, 0)">
                  <rect x="0" y="0" width="400" height="48" rx="8" fill={PAPER_CREAM} stroke={STONE_GREY} strokeWidth="2" />
                  <text x="16" y="32" fill={INK_CHARCOAL} fontSize="19" fontWeight="900" fontFamily="sans-serif">SOLAR POWER</text>
                  <text x="384" y="32" textAnchor="end" fill={SAGE_GREEN} fontSize="19" fontWeight="900" fontFamily="monospace">RESTORES 100%</text>
                </g>
                <g transform="translate(0, 60)">
                  <rect x="0" y="0" width="400" height="48" rx="8" fill={PAPER_CREAM} stroke={STONE_GREY} strokeWidth="2" />
                  <text x="16" y="32" fill={INK_CHARCOAL} fontSize="19" fontWeight="900" fontFamily="sans-serif">BREACH HAZARD</text>
                  <text x="384" y="32" textAnchor="end" fill={MUTED_BURGUNDY} fontSize="19" fontWeight="900" fontFamily="monospace">80% RISK</text>
                </g>
                <g transform="translate(0, 120)">
                  <rect x="0" y="0" width="400" height="48" rx="8" fill={PAPER_CREAM} stroke={STONE_GREY} strokeWidth="2" />
                  <text x="16" y="32" fill={INK_CHARCOAL} fontSize="19" fontWeight="900" fontFamily="sans-serif">CONDITIONS</text>
                  <text x="384" y="32" textAnchor="end" fill={INK_CHARCOAL} fontSize="18" fontWeight="800" fontFamily="monospace">100 KM/H WIND</text>
                </g>
                <g transform="translate(0, 180)">
                  <rect x="0" y="0" width="400" height="50" rx="8" fill={INK_CHARCOAL} />
                  <text x="200" y="32" textAnchor="middle" fill={WARM_GOLD} fontSize="18" fontWeight="900" fontFamily="sans-serif">
                    VOTE A IN COMMENTS
                  </text>
                </g>
              </g>
            </g>

            {/* Protocol [ B ]: CRYO-HIBERNATION */}
            <g transform="translate(555, 380)">
              <rect
                x="0"
                y="0"
                width="460"
                height="560"
                rx="18"
                fill="#EAE4D8"
                stroke={MUTED_BLUE}
                strokeWidth="6"
              />
              <rect x="22" y="22" width="416" height="60" rx="10" fill={MUTED_BLUE} />
              <text x="230" y="62" textAnchor="middle" fill={PAPER_CREAM} fontSize="24" fontWeight="900" fontFamily="sans-serif">
                [ B ] CRYO-HIBERNATE
              </text>

              {/* Handcrafted Cryo Capsule Pod Illustration */}
              <g transform="translate(145, 120)">
                <rect x="0" y="0" width="170" height="110" rx="12" fill={PAPER_CREAM} stroke={INK_CHARCOAL} strokeWidth="4" />
                <ellipse cx="85" cy="55" rx="60" ry="32" fill="#D0DEEB" stroke={MUTED_BLUE} strokeWidth="3" />
                <line x1="35" y1="55" x2="135" y2="55" stroke={MUTED_BLUE} strokeWidth="3" strokeDasharray="6 4" />
              </g>

              {/* Outcome Telemetry Rows */}
              <g transform="translate(30, 265)">
                <g transform="translate(0, 0)">
                  <rect x="0" y="0" width="400" height="48" rx="8" fill={PAPER_CREAM} stroke={STONE_GREY} strokeWidth="2" />
                  <text x="16" y="32" fill={INK_CHARCOAL} fontSize="19" fontWeight="900" fontFamily="sans-serif">ENERGY USE</text>
                  <text x="384" y="32" textAnchor="end" fill={MUTED_BLUE} fontSize="19" fontWeight="900" fontFamily="monospace">-90% CUT</text>
                </g>
                <g transform="translate(0, 60)">
                  <rect x="0" y="0" width="400" height="48" rx="8" fill={PAPER_CREAM} stroke={STONE_GREY} strokeWidth="2" />
                  <text x="16" y="32" fill={INK_CHARCOAL} fontSize="19" fontWeight="900" fontFamily="sans-serif">TEMPERATURE</text>
                  <text x="384" y="32" textAnchor="end" fill={MUTED_BURGUNDY} fontSize="19" fontWeight="900" fontFamily="monospace">-85°C FREEZING</text>
                </g>
                <g transform="translate(0, 120)">
                  <rect x="0" y="0" width="400" height="48" rx="8" fill={PAPER_CREAM} stroke={STONE_GREY} strokeWidth="2" />
                  <text x="16" y="32" fill={INK_CHARCOAL} fontSize="19" fontWeight="900" fontFamily="sans-serif">SANCTUARY</text>
                  <text x="384" y="32" textAnchor="end" fill={INK_CHARCOAL} fontSize="18" fontWeight="800" fontFamily="monospace">ROVER POD</text>
                </g>
                <g transform="translate(0, 180)">
                  <rect x="0" y="0" width="400" height="50" rx="8" fill={INK_CHARCOAL} />
                  <text x="200" y="32" textAnchor="middle" fill={WARM_GOLD} fontSize="18" fontWeight="900" fontFamily="sans-serif">
                    VOTE B IN COMMENTS
                  </text>
                </g>
              </g>
            </g>

            {/* Bottom Emergency Countdown Seal */}
            <g transform="translate(240, 1195)">
              <rect x="0" y="0" width="600" height="75" rx="14" fill={INK_CHARCOAL} stroke={DUSTY_CORAL} strokeWidth="4" />
              <text x="300" y="46" textAnchor="middle" fill={PAPER_CREAM} fontSize="22" fontWeight="900" fontFamily="monospace">
                DECISION TIMER: 00:0{Math.max(1, 4 - Math.floor((frame % 120) / 30))} // VOTE NOW!
              </text>
            </g>
          </>
        )}
      </svg>
    </div>
  );
};
