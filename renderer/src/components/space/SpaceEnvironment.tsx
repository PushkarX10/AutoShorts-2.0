import React from "react";
import { useCurrentFrame } from "remotion";

interface SpaceEnvironmentProps {
  environment: string;
  planet?: "mars" | "moon" | "jupiter" | "venus" | "titan" | "deep_space";
  sceneId: number;
}

export const SpaceEnvironment: React.FC<SpaceEnvironmentProps> = ({
  environment,
  planet = "mars",
  sceneId,
}) => {
  const frame = useCurrentFrame();

  // Controlled Palette strictly from project specification:
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
  const MUTED_GREY = "#A4AFC0";

  // Particle & dynamic animations
  const starPulse = Math.sin(frame * 0.1) * 0.3 + 0.7;
  const dustShift = (frame * 18) % 1920;
  const stormDrift = (frame * 35) % 1920;
  const sunPulse = Math.sin(frame * 0.05) * 6;

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
          {/* Space Sky Gradient (Deep Space Navy to Space Black) */}
          <linearGradient id="space-sky" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#05070D" />
            <stop offset="45%" stopColor={DEEP_SPACE_NAVY} />
            <stop offset="70%" stopColor="#2A1B28" />
            <stop offset="100%" stopColor="#4A2620" />
          </linearGradient>

          {/* Mars Red Sand Dunes Gradient */}
          <linearGradient id="mars-dunes" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor={PLANETARY_ORANGE} />
            <stop offset="35%" stopColor={MARS_RED} />
            <stop offset="85%" stopColor="#7A2D22" />
            <stop offset="100%" stopColor="#2D110D" />
          </linearGradient>

          {/* Distant Mountains Gradient */}
          <linearGradient id="mars-mountains" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#8C3A2C" />
            <stop offset="100%" stopColor="#2B141E" />
          </linearGradient>

          {/* Solar Star Glint */}
          <radialGradient id="sun-glint" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#FFFBEB" stopOpacity="1" />
            <stop offset="30%" stopColor={SOLAR_YELLOW} stopOpacity="0.8" />
            <stop offset="70%" stopColor={PLANETARY_ORANGE} stopOpacity="0.25" />
            <stop offset="100%" stopColor="#080B14" stopOpacity="0" />
          </radialGradient>

          {/* Geodesic Dome Glow */}
          <radialGradient id="dome-interior-glow" cx="50%" cy="65%" r="60%">
            <stop offset="0%" stopColor={ELECTRIC_CYAN} stopOpacity="0.45" />
            <stop offset="60%" stopColor={MIDNIGHT_BLUE} stopOpacity="0.25" />
            <stop offset="100%" stopColor="#080B14" stopOpacity="0" />
          </radialGradient>
        </defs>

        {/* --- BASE SKY BACKGROUND --- */}
        <rect x="0" y="0" width="1080" height="1920" fill="url(#space-sky)" />

        {/* --- TWINKLING STARS IN DEEP SPACE --- */}
        <g opacity={starPulse}>
          {[
            [120, 180, 2], [240, 95, 2.5], [420, 210, 1.5], [680, 140, 2],
            [890, 80, 3], [1010, 240, 1.8], [80, 390, 2], [320, 480, 2.5],
            [740, 420, 2.2], [960, 490, 1.8], [510, 310, 3], [180, 620, 2],
            [880, 600, 2.5], [620, 710, 1.5], [380, 780, 2],
          ].map(([sx, sy, sr], i) => (
            <circle key={i} cx={sx} cy={sy} r={sr} fill={WHITE} />
          ))}
        </g>

        {/* Distant Pale Sun (Appears smaller on Mars: 68% of Earth size) */}
        <g transform="translate(860, 220)">
          <circle cx="0" cy="0" r={45 + sunPulse} fill="url(#sun-glint)" />
          <circle cx="0" cy="0" r="14" fill="#FFFFFF" />
        </g>

        {/* Mars' Tiny Potato-shaped Moon: Phobos */}
        <g transform="translate(240, 280)">
          <ellipse cx="0" cy="0" rx="18" ry="12" fill={STEEL_BLUE} stroke={SPACE_BLACK} strokeWidth="3" transform="rotate(-25)" />
          <circle cx="-5" cy="-2" r="3.5" fill="#2B3A4F" />
          <circle cx="6" cy="3" r="2.5" fill="#2B3A4F" />
        </g>

        {/* ========================================================================= */}
        {/* SCENE 1 & 3: MARS SURFACE HORIZON & OLYMPUS MONS VOLCANO                  */}
        {/* ========================================================================= */}
        {(environment === "mars_surface" || environment === "mars_arrival") && (
          <>
            {/* Distant Mountain Ridge (Olympus Mons silhouette) */}
            <path
              d="M -50 950 Q 280 840 540 820 Q 800 840 1130 950 L 1130 1350 L -50 1350 Z"
              fill="url(#mars-mountains)"
              stroke={SPACE_BLACK}
              strokeWidth="6"
            />

            {/* Midground Rocky Crags */}
            <polygon
              points="-40,1120 180,1030 380,1080 620,1010 880,1070 1120,1020 1120,1400 -40,1400"
              fill="#52241C"
              stroke={SPACE_BLACK}
              strokeWidth="6"
            />

            {/* Foreground Mars Red Sand Dunes */}
            <path
              d="M -40 1260 Q 280 1210 540 1270 Q 820 1310 1120 1250 L 1120 1920 L -40 1920 Z"
              fill="url(#mars-dunes)"
              stroke={SPACE_BLACK}
              strokeWidth="10"
            />

            {/* Surface Rocks and Impact Boulders */}
            <g fill="#4A1E17" stroke={SPACE_BLACK} strokeWidth="5">
              <ellipse cx="140" cy="1285" rx="34" ry="16" />
              <ellipse cx="880" cy="1295" rx="42" ry="20" />
              <ellipse cx="680" cy="1320" rx="22" ry="11" />
            </g>

            {/* Swirling Martian Dust Devil Particles */}
            <g opacity="0.45">
              {[...Array(16)].map((_, i) => {
                const px = ((dustShift + i * 85) % 1150) - 50;
                const py = 1200 + Math.sin(frame * 0.1 + i) * 35 + (i % 4) * 20;
                return (
                  <ellipse key={i} cx={px} cy={py} rx={16 + i * 2} ry="4" fill={PLANETARY_ORANGE} />
                );
              })}
            </g>
          </>
        )}

        {/* ========================================================================= */}
        {/* SCENE 2: SCIENTIFIC INFOGRAPHIC — EARTH VS MARS COMPARISON                */}
        {/* ========================================================================= */}
        {environment === "planet_comparison" && (
          <>
            <rect x="0" y="0" width="1080" height="1920" fill={SPACE_BLACK} />

            {/* Infographic Header Pill */}
            <g transform="translate(140, 260)">
              <rect x="0" y="0" width="800" height="75" rx="14" fill={DEEP_SPACE_NAVY} stroke={STEEL_BLUE} strokeWidth="4" />
              <text x="400" y="48" textAnchor="middle" fill={WHITE} fontSize="26" fontWeight="900" letterSpacing="4px" fontFamily="sans-serif">
                PLANETARY TELEMETRY // COMPARISON
              </text>
            </g>

            {/* Left Card: PLANET EARTH (1.0g) */}
            <g transform="translate(80, 370)">
              <rect x="0" y="0" width="430" height="840" rx="22" fill={MIDNIGHT_BLUE} stroke={ELECTRIC_CYAN} strokeWidth="6" />
              <rect x="25" y="25" width="380" height="60" rx="10" fill={ELECTRIC_CYAN} />
              <text x="215" y="66" textAnchor="middle" fill={SPACE_BLACK} fontSize="26" fontWeight="900" fontFamily="sans-serif">
                EARTH (HOME)
              </text>

              {/* 2D Vector Earth Illustration */}
              <g transform="translate(215, 230)">
                <circle cx="0" cy="0" r="105" fill="#1C658C" stroke={SPACE_BLACK} strokeWidth="6" />
                {/* Continents in Green */}
                <path d="M -50 -40 Q -20 -80 30 -50 Q 60 -10 20 20 Q -40 60 -50 -40 Z" fill={OXYGEN_GREEN} />
                <path d="M 20 25 Q 60 40 40 80 Q 0 70 20 25 Z" fill={OXYGEN_GREEN} />
                {/* Atmospheric Glow */}
                <circle cx="0" cy="0" r="112" fill="none" stroke={ELECTRIC_CYAN} strokeWidth="4" opacity="0.6" />
              </g>

              {/* Earth Metrics */}
              <g transform="translate(35, 410)">
                <text x="0" y="0" fill={ELECTRIC_CYAN} fontSize="22" fontWeight="900" fontFamily="sans-serif">GRAVITY: 1.0g (100%)</text>
                <text x="0" y="45" fill={WHITE} fontSize="20" fontWeight="800" fontFamily="sans-serif">PRESSURE: 1.0 ATM</text>
                <text x="0" y="90" fill={OXYGEN_GREEN} fontSize="20" fontWeight="800" fontFamily="sans-serif">OXYGEN: 21% (BREATHABLE)</text>
                <text x="0" y="135" fill={SOLAR_YELLOW} fontSize="20" fontWeight="800" fontFamily="sans-serif">TEMP: +15°C (AVERAGE)</text>
                <text x="0" y="180" fill={MUTED_GREY} fontSize="18" fontWeight="800" fontFamily="monospace">WATER: 71% OCEANS</text>
              </g>
            </g>

            {/* Right Card: PLANET MARS (0.38g) */}
            <g transform="translate(570, 370)">
              <rect x="0" y="0" width="430" height="840" rx="22" fill={MIDNIGHT_BLUE} stroke={MARS_RED} strokeWidth="6" />
              <rect x="25" y="25" width="380" height="60" rx="10" fill={MARS_RED} />
              <text x="215" y="66" textAnchor="middle" fill={WHITE} fontSize="26" fontWeight="900" fontFamily="sans-serif">
                MARS (SOL 18)
              </text>

              {/* 2D Vector Mars Illustration (Approx 53% diameter of Earth) */}
              <g transform="translate(215, 230)">
                <circle cx="0" cy="0" r="65" fill={MARS_RED} stroke={SPACE_BLACK} strokeWidth="6" />
                {/* Dark basaltic maria */}
                <ellipse cx="-15" cy="-10" rx="25" ry="14" fill="#6A271C" />
                <ellipse cx="20" cy="18" rx="20" ry="10" fill="#6A271C" />
                {/* White Polar Ice Cap */}
                <ellipse cx="0" cy="-58" rx="24" ry="7" fill={WHITE} />
              </g>

              {/* Mars Metrics */}
              <g transform="translate(35, 410)">
                <text x="0" y="0" fill={PLANETARY_ORANGE} fontSize="22" fontWeight="900" fontFamily="sans-serif">GRAVITY: 0.38g (38%)</text>
                <text x="0" y="45" fill={MARS_RED} fontSize="20" fontWeight="900" fontFamily="sans-serif">PRESSURE: 0.006 ATM</text>
                <text x="0" y="90" fill={MARS_RED} fontSize="20" fontWeight="900" fontFamily="sans-serif">ATMOSPHERE: 95% CO2</text>
                <text x="0" y="135" fill={ELECTRIC_CYAN} fontSize="20" fontWeight="800" fontFamily="sans-serif">TEMP: -63°C (FREEZING)</text>
                <text x="0" y="180" fill={MUTED_GREY} fontSize="18" fontWeight="800" fontFamily="monospace">WATER: 0% (FROZEN ICE)</text>
              </g>
            </g>

            {/* Bottom Science Fact Callout */}
            <g transform="translate(80, 1240)">
              <rect x="0" y="0" width="920" height="65" rx="12" fill={DEEP_SPACE_NAVY} stroke={STEEL_BLUE} strokeWidth="3" />
              <text x="460" y="42" textAnchor="middle" fill={SOLAR_YELLOW} fontSize="20" fontWeight="900" fontFamily="monospace">
                SUIT BREACH = BLOOD BOILS AT BODY TEMP IN 10 SECONDS
              </text>
            </g>
          </>
        )}

        {/* ========================================================================= */}
        {/* SCENE 4: GEODESIC MARS BASE HABITAT & SOLAR ARRAYS                        */}
        {/* ========================================================================= */}
        {environment === "mars_habitat" && (
          <>
            {/* Distant Hills */}
            <path d="M -40 1080 Q 300 980 600 1020 Q 900 980 1120 1060 L 1120 1350 L -40 1350 Z" fill="#6A291E" stroke={SPACE_BLACK} strokeWidth="6" />

            {/* Pressurized Geodesic Habitat Dome */}
            <g transform="translate(540, 1260)">
              {/* Outer Dome Shell */}
              <path
                d="M -340 0 C -340 -260, 340 -260, 340 0 Z"
                fill={DEEP_SPACE_NAVY}
                stroke={STEEL_BLUE}
                strokeWidth="10"
              />
              {/* Interior Glow */}
              <path d="M -330 -5 C -330 -250, 330 -250, 330 -5 Z" fill="url(#dome-interior-glow)" />

              {/* Geodesic Hexagonal Lattice Struts */}
              <g stroke={STEEL_BLUE} strokeWidth="4" opacity="0.6">
                <line x1="-240" y1="-80" x2="-140" y2="-180" />
                <line x1="-140" y1="-180" x2="0" y2="-230" />
                <line x1="0" y1="-230" x2="140" y2="-180" />
                <line x1="140" y1="-180" x2="240" y2="-80" />
                <line x1="-240" y1="-80" x2="-140" y2="0" />
                <line x1="-140" y1="0" x2="0" y2="-100" />
                <line x1="0" y1="-100" x2="140" y2="0" />
                <line x1="140" y1="0" x2="240" y2="-80" />
              </g>

              {/* Glowing Airlock Module */}
              <rect x="-70" y="-120" width="140" height="120" rx="14" fill="#0E1626" stroke={ELECTRIC_CYAN} strokeWidth="6" />
              <circle cx="0" cy="-60" r="28" fill="#182744" stroke={ELECTRIC_CYAN} strokeWidth="4" />
              <line x1="0" y1="-75" x2="0" y2="-45" stroke={ELECTRIC_CYAN} strokeWidth="4" />
              <line x1="-15" y1="-60" x2="15" y2="-60" stroke={ELECTRIC_CYAN} strokeWidth="4" />
              <text x="0" y="-15" textAnchor="middle" fill={ELECTRIC_CYAN} fontSize="14" fontWeight="900" fontFamily="monospace">AIRLOCK 01</text>
            </g>

            {/* Solar Panel Array Units */}
            <g transform="translate(80, 1180)" fill="#102538" stroke={SPACE_BLACK} strokeWidth="5">
              <polygon points="0,70 180,30 240,80 60,120" />
              {/* Blue solar grid lines */}
              <line x1="45" y1="60" x2="105" y2="105" stroke={ELECTRIC_CYAN} strokeWidth="2" />
              <line x1="90" y1="50" x2="150" y2="95" stroke={ELECTRIC_CYAN} strokeWidth="2" />
              <line x1="135" y1="40" x2="195" y2="85" stroke={ELECTRIC_CYAN} strokeWidth="2" />
              {/* Stand */}
              <line x1="120" y1="80" x2="120" y2="140" stroke={SPACE_BLACK} strokeWidth="8" />
            </g>

            {/* Ground Dunes */}
            <polygon points="-40,1260 1120,1260 1120,1920 -40,1920" fill="url(#mars-dunes)" />
            <line x1="-40" y1="1260" x2="1120" y2="1260" stroke={SPACE_BLACK} strokeWidth="10" />
          </>
        )}

        {/* ========================================================================= */}
        {/* SCENE 5: SOL 18 DUST STORM CRISIS (85% POWER LOSS)                       */}
        {/* ========================================================================= */}
        {environment === "mars_dust_storm" && (
          <>
            {/* Blotted Out Dark Sky */}
            <rect x="0" y="0" width="1080" height="1920" fill="#2E1410" />

            {/* Giant Swirling Sandstorm Cloud Front */}
            <g opacity="0.85">
              <path
                d="M -50 300 Q 240 220 540 340 Q 840 200 1130 310 L 1130 1400 L -50 1400 Z"
                fill="#8C3524"
              />
              <path
                d="M -50 500 Q 300 420 600 520 Q 900 450 1130 540 L 1130 1400 L -50 1400 Z"
                fill="#C65B45"
              />
            </g>

            {/* Rapid Horizontal 100 km/h Wind Dust Streaks */}
            <g stroke={PLANETARY_ORANGE} opacity="0.65">
              {[...Array(24)].map((_, i) => {
                const wx = ((stormDrift + i * 90) % 1500) - 300;
                const wy = 400 + ((i * 55) % 900);
                const wLen = 140 + (i % 5) * 40;
                return (
                  <line
                    key={i}
                    x1={wx}
                    y1={wy}
                    x2={wx + wLen}
                    y2={wy + 15}
                    strokeWidth={3 + (i % 3)}
                    strokeLinecap="round"
                  />
                );
              })}
            </g>

            {/* Covered Solar Panels Failing */}
            <g transform="translate(180, 1180)" fill="#4A251C" stroke={SPACE_BLACK} strokeWidth="5">
              <polygon points="0,70 180,30 240,80 60,120" />
              {/* Thick red dust coating */}
              <polygon points="10,68 175,32 230,78 55,115" fill={MARS_RED} opacity="0.85" />
              {/* Alert Sign */}
              <g transform="translate(120, 20)">
                <circle cx="0" cy="0" r="16" fill={MARS_RED} />
                <text x="0" y="5" textAnchor="middle" fill={WHITE} fontSize="16" fontWeight="900">!</text>
              </g>
            </g>

            {/* Ground Dunes */}
            <polygon points="-40,1260 1120,1260 1120,1920 -40,1920" fill="#4D1A14" />
            <line x1="-40" y1="1260" x2="1120" y2="1260" stroke={SPACE_BLACK} strokeWidth="10" />
          </>
        )}

        {/* ========================================================================= */}
        {/* SCENE 6: INTERACTIVE SURVIVAL PROTOCOL CLIFFHANGER (A vs B)              */}
        {/* ========================================================================= */}
        {environment === "space_cliffhanger" && (
          <>
            <rect x="0" y="0" width="1080" height="1920" fill={SPACE_BLACK} />

            {/* Main Decision Banner */}
            <g transform="translate(60, 360)">
              <rect x="0" y="0" width="960" height="85" rx="16" fill={DEEP_SPACE_NAVY} stroke={STEEL_BLUE} strokeWidth="5" />
              <text x="480" y="55" textAnchor="middle" fill={WHITE} fontSize="28" fontWeight="900" letterSpacing="4px" fontFamily="sans-serif">
                WHAT WOULD YOU DO TO SURVIVE?
              </text>

              {/* Protocol [ A ]: BRAVE THE STORM */}
              <g transform="translate(0, 120)">
                <rect
                  x="0"
                  y="0"
                  width="460"
                  height="450"
                  rx="22"
                  fill={MIDNIGHT_BLUE}
                  stroke={PLANETARY_ORANGE}
                  strokeWidth="8"
                  style={{ filter: `drop-shadow(0 0 ${16 + Math.sin(frame * 0.4) * 8}px #F18B45)` }}
                />
                <rect x="25" y="25" width="410" height="60" rx="10" fill={PLANETARY_ORANGE} />
                <text x="230" y="66" textAnchor="middle" fill={SPACE_BLACK} fontSize="24" fontWeight="900" fontFamily="sans-serif">
                  [ A ] BRAVE THE STORM
                </text>

                {/* Solar Panel & Dust Icon */}
                <g transform="translate(135, 140)">
                  <polygon points="0,50 140,20 180,60 40,90" fill="#182744" stroke={PLANETARY_ORANGE} strokeWidth="5" />
                  <line x1="90" y1="60" x2="90" y2="110" stroke={WHITE} strokeWidth="6" />
                </g>

                <g transform="translate(35, 290)">
                  <text x="0" y="0" fill={PLANETARY_ORANGE} fontSize="20" fontWeight="900" fontFamily="sans-serif">POWER: RESTORES 100%</text>
                  <text x="0" y="45" fill={MARS_RED} fontSize="19" fontWeight="900" fontFamily="sans-serif">SUIT BREACH RISK: 80%</text>
                  <text x="0" y="85" fill={WHITE} fontSize="17" fontWeight="800" fontFamily="sans-serif">100 KM/H SANDSTORM</text>
                  <text x="0" y="125" fill={MUTED_GREY} fontSize="15" fontWeight="800" fontFamily="monospace">MANUAL PANEL BRUSHING</text>
                </g>
              </g>

              {/* Protocol [ B ]: CRYO-HIBERNATION */}
              <g transform="translate(500, 120)">
                <rect
                  x="0"
                  y="0"
                  width="460"
                  height="450"
                  rx="22"
                  fill={MIDNIGHT_BLUE}
                  stroke={ELECTRIC_CYAN}
                  strokeWidth="8"
                  style={{ filter: `drop-shadow(0 0 ${16 + Math.sin(frame * 0.4 + 1) * 8}px #55D7E8)` }}
                />
                <rect x="25" y="25" width="410" height="60" rx="10" fill={ELECTRIC_CYAN} />
                <text x="230" y="66" textAnchor="middle" fill={SPACE_BLACK} fontSize="24" fontWeight="900" fontFamily="sans-serif">
                  [ B ] CRYO-HIBERNATE
                </text>

                {/* Cryo Pod Icon */}
                <g transform="translate(145, 130)">
                  <rect x="0" y="0" width="160" height="90" rx="18" fill="#10182A" stroke={ELECTRIC_CYAN} strokeWidth="5" />
                  <ellipse cx="80" cy="45" rx="55" ry="24" fill={ELECTRIC_CYAN} opacity="0.3" />
                  <line x1="30" y1="45" x2="130" y2="45" stroke={ELECTRIC_CYAN} strokeWidth="3" strokeDasharray="6 4" />
                </g>

                <g transform="translate(35, 290)">
                  <text x="0" y="0" fill={ELECTRIC_CYAN} fontSize="20" fontWeight="900" fontFamily="sans-serif">ENERGY USE: -90% CUT</text>
                  <text x="0" y="45" fill={MARS_RED} fontSize="19" fontWeight="900" fontFamily="sans-serif">FREEZING RISK: -80°C</text>
                  <text x="0" y="85" fill={WHITE} fontSize="17" fontWeight="800" fontFamily="sans-serif">ROVER SLEEP POD</text>
                  <text x="0" y="125" fill={MUTED_GREY} fontSize="15" fontWeight="800" fontFamily="monospace">HEATERS SHUT OFF</text>
                </g>
              </g>

              {/* Emergency Countdown Indicator */}
              <g transform="translate(240, 610)">
                <rect x="0" y="0" width="480" height="65" rx="14" fill={SPACE_BLACK} stroke={MARS_RED} strokeWidth="4" />
                <text x="240" y="42" textAnchor="middle" fill={MARS_RED} fontSize="22" fontWeight="900" fontFamily="monospace">
                  OXYGEN SYSTEM SHUTDOWN: 00:0{Math.max(1, 4 - Math.floor((frame % 120) / 30))}
                </text>
              </g>
            </g>

            {/* Floor */}
            <polygon points="-40,1260 1120,1260 1120,1920 -40,1920" fill="#080B14" />
            <line x1="-40" y1="1260" x2="1120" y2="1260" stroke={STEEL_BLUE} strokeWidth="10" />
          </>
        )}
      </svg>
    </div>
  );
};
