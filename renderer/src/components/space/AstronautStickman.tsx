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
  y?: number; // 0.0 to 1.0 (vertical center)
  scale?: number;
  facing?: "left" | "right";
  suitColor?: string;
  outlineColor?: string;
  visorTint?: string;
}

/**
 * Handcrafted 2D Illustrated Astronaut Mascot
 * Editorial Science-Journal Aesthetic:
 * - Organic, slightly hand-inked contours with natural variation
 * - Friendly circular helmet with distinctive vintage exploration bubble
 * - Expressive eyes and eyebrows visible through the visor
 * - Tailored off-white spacesuit with charcoal seams, patches, and chest life-support pack
 * - Flexible, articulate limbs with weighted moon boots
 */
export const AstronautStickman: React.FC<AstronautProps> = ({
  pose = "walk_explore",
  expression = "focused",
  x = 0.5,
  y = 0.5,
  scale = 1.0,
  facing = "right",
  suitColor = "#F4EFE5",     // Paper Cream suit
  outlineColor = "#242B35",  // Ink Charcoal lines
  visorTint = "#527A9B",     // Muted Blue visor
}) => {
  const frame = useCurrentFrame();

  // Natural breathing & floating oscillations
  const breath = Math.sin(frame * 0.1) * 3;
  const floatY = pose === "idle_float" ? Math.sin(frame * 0.07) * 20 : 0;
  const floatRot = pose === "idle_float" ? Math.sin(frame * 0.05) * 5 : 0;

  // Mars low-gravity jump physics (0.38g buoyant arc)
  const jumpPhase = (frame * 0.12) % Math.PI;
  const jumpY = pose === "low_gravity_jump" ? -Math.sin(jumpPhase) * 80 : 0;

  // Walking cycle with low-gravity bounce
  const walkPhase = frame * 0.2;
  const legFront = pose === "walk_explore" ? Math.sin(walkPhase) * 32 : 0;
  const legBack = pose === "walk_explore" ? -Math.sin(walkPhase) * 32 : 0;
  const armFront = pose === "walk_explore" ? -Math.sin(walkPhase) * 26 : 0;
  const armBack = pose === "walk_explore" ? Math.sin(walkPhase) * 26 : 0;

  // Panic tremor for emergency low O2
  const tremor = pose === "panic_o2" ? Math.sin(frame * 0.9) * 4 : 0;

  // Visor gold reflection shimmer
  const visorShimmer = Math.sin(frame * 0.08) * 15;

  const flipH = facing === "left" ? -1 : 1;

  // Palette from v2.0 spec
  const PAPER_CREAM = suitColor;
  const INK_CHARCOAL = outlineColor;
  const DUSTY_CORAL = "#C86D52";
  const MUTED_BLUE = visorTint;
  const WARM_GOLD = "#D5AA62";
  const SAGE_GREEN = "#768C79";

  return (
    <div
      style={{
        position: "absolute",
        left: `${x * 100}%`,
        top: `${y * 100}%`,
        transform: `translate(-50%, -50%) translate(${tremor}px, ${floatY + jumpY}px) rotate(${floatRot}deg) scale(${scale}) scaleX(${flipH})`,
        width: 360,
        height: 540,
        pointerEvents: "none",
        zIndex: 35,
      }}
    >
      <svg
        viewBox="0 0 360 540"
        style={{ width: "100%", height: "100%", overflow: "visible" }}
      >
        <defs>
          {/* Subtle hand-drawn drop shadow */}
          <filter id="hand-drawn-shadow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="10" stdDeviation="8" floodColor="rgba(36,43,53,0.35)" />
          </filter>

          {/* Visor Gradient: Muted Blue to Deep Ink */}
          <linearGradient id="editorial-visor" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#7FA3C2" stopOpacity="0.85" />
            <stop offset="50%" stopColor={MUTED_BLUE} stopOpacity="0.92" />
            <stop offset="100%" stopColor={INK_CHARCOAL} stopOpacity="0.98" />
          </linearGradient>

          {/* Golden Sun Glint on Helmet */}
          <linearGradient id="visor-glint" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#FFFFFF" stopOpacity="0.85" />
            <stop offset="40%" stopColor={WARM_GOLD} stopOpacity="0.5" />
            <stop offset="100%" stopColor="transparent" stopOpacity="0" />
          </linearGradient>
        </defs>

        {/* ========================================================================= */}
        {/* 1. LIFE SUPPORT BACKPACK (Mounted behind character)                       */}
        {/* ========================================================================= */}
        <g transform={`translate(100, ${185 + breath})`} filter="url(#hand-drawn-shadow)">
          {/* Backpack Box with rounded hand-drawn corners */}
          <rect
            x="0"
            y="0"
            width="55"
            height="115"
            rx="12"
            fill="#E5DDD0"
            stroke={INK_CHARCOAL}
            strokeWidth="5"
            strokeLinejoin="round"
          />
          {/* Oxygen Tank Cylinders */}
          <rect
            x="8"
            y="12"
            width="16"
            height="90"
            rx="8"
            fill="#D0C6B5"
            stroke={INK_CHARCOAL}
            strokeWidth="3.5"
          />
          <rect
            x="30"
            y="12"
            width="16"
            height="90"
            rx="8"
            fill="#D0C6B5"
            stroke={INK_CHARCOAL}
            strokeWidth="3.5"
          />
          {/* Tank Pressure Rings */}
          <line x1="8" y1="45" x2="24" y2="45" stroke={INK_CHARCOAL} strokeWidth="3" />
          <line x1="30" y1="45" x2="46" y2="45" stroke={INK_CHARCOAL} strokeWidth="3" />
          {/* Scientific Identification Stripe */}
          <rect x="0" y="80" width="55" height="12" fill={DUSTY_CORAL} />

          {/* Dual Flexible Oxygen Feed Hoses */}
          <path
            d="M 28 105 Q 40 140 75 145"
            fill="none"
            stroke={INK_CHARCOAL}
            strokeWidth="6"
            strokeLinecap="round"
          />
          <path
            d="M 28 105 Q 40 140 75 145"
            fill="none"
            stroke={PAPER_CREAM}
            strokeWidth="2.5"
            strokeDasharray="4 3"
          />
        </g>

        {/* ========================================================================= */}
        {/* 2. BACK ARM (Walking / Gesturing Layer)                                  */}
        {/* ========================================================================= */}
        <g transform={`translate(160, ${210 + breath})`}>
          {pose === "walk_explore" && (
            <g transform={`rotate(${armBack}, 0, 0)`}>
              <path
                d="M 0 0 Q -25 45 -35 85"
                fill="none"
                stroke={INK_CHARCOAL}
                strokeWidth="18"
                strokeLinecap="round"
              />
              <path
                d="M 0 0 Q -25 45 -35 85"
                fill="none"
                stroke={PAPER_CREAM}
                strokeWidth="11"
                strokeLinecap="round"
              />
              {/* Suit Joint Ribs */}
              <circle cx="-18" cy="40" r="11" fill="none" stroke={INK_CHARCOAL} strokeWidth="3" />
              {/* Glove */}
              <ellipse cx="-35" cy="88" rx="14" ry="12" fill={INK_CHARCOAL} />
            </g>
          )}

          {pose === "panic_o2" && (
            <g transform="rotate(-70, 0, 0)">
              <path
                d="M 0 0 Q -20 40 -15 80"
                fill="none"
                stroke={INK_CHARCOAL}
                strokeWidth="18"
                strokeLinecap="round"
              />
              <path
                d="M 0 0 Q -20 40 -15 80"
                fill="none"
                stroke={PAPER_CREAM}
                strokeWidth="11"
                strokeLinecap="round"
              />
              <ellipse cx="-15" cy="85" rx="14" ry="12" fill={INK_CHARCOAL} />
            </g>
          )}

          {pose === "point_sky" && (
            <g transform="rotate(25, 0, 0)">
              <path
                d="M 0 0 Q -20 45 -25 80"
                fill="none"
                stroke={INK_CHARCOAL}
                strokeWidth="18"
                strokeLinecap="round"
              />
              <path
                d="M 0 0 Q -20 45 -25 80"
                fill="none"
                stroke={PAPER_CREAM}
                strokeWidth="11"
                strokeLinecap="round"
              />
              <ellipse cx="-25" cy="85" rx="14" ry="12" fill={INK_CHARCOAL} />
            </g>
          )}
        </g>

        {/* ========================================================================= */}
        {/* 3. LEGS & MOON BOOTS (Organic hand-drawn joints)                         */}
        {/* ========================================================================= */}
        <g transform="translate(180, 310)">
          {/* Back Leg */}
          <g transform={`rotate(${legBack}, 0, 0)`}>
            {/* Upper Thigh */}
            <path
              d="M -15 0 Q -25 55 -28 95"
              fill="none"
              stroke={INK_CHARCOAL}
              strokeWidth="22"
              strokeLinecap="round"
            />
            <path
              d="M -15 0 Q -25 55 -28 95"
              fill="none"
              stroke={PAPER_CREAM}
              strokeWidth="14"
              strokeLinecap="round"
            />
            {/* Knee Joint Band */}
            <line x1="-34" y1="52" x2="-18" y2="52" stroke={INK_CHARCOAL} strokeWidth="4" />

            {/* Lower Shin */}
            <path
              d="M -28 95 Q -32 135 -35 160"
              fill="none"
              stroke={INK_CHARCOAL}
              strokeWidth="20"
              strokeLinecap="round"
            />
            <path
              d="M -28 95 Q -32 135 -35 160"
              fill="none"
              stroke={PAPER_CREAM}
              strokeWidth="12"
              strokeLinecap="round"
            />

            {/* Chunky Illustrated Moon Boot */}
            <g transform="translate(-50, 150)">
              <path
                d="M 5 10 L 25 10 Q 32 10 32 25 L 32 38 Q 32 45 22 45 L -8 45 Q -14 45 -14 36 L -10 24 Q -6 10 5 10 Z"
                fill={INK_CHARCOAL}
              />
              {/* Boot Sole Tread */}
              <rect x="-14" y="40" width="46" height="8" rx="3" fill="#3D4552" />
              <line x1="-8" y1="44" x2="26" y2="44" stroke={WARM_GOLD} strokeWidth="2.5" />
            </g>
          </g>

          {/* Front Leg */}
          <g transform={`rotate(${legFront}, 0, 0)`}>
            {/* Upper Thigh */}
            <path
              d="M 15 0 Q 25 55 28 95"
              fill="none"
              stroke={INK_CHARCOAL}
              strokeWidth="24"
              strokeLinecap="round"
            />
            <path
              d="M 15 0 Q 25 55 28 95"
              fill="none"
              stroke={PAPER_CREAM}
              strokeWidth="15"
              strokeLinecap="round"
            />
            {/* Knee Joint Band */}
            <line x1="18" y1="52" x2="34" y2="52" stroke={INK_CHARCOAL} strokeWidth="4" />

            {/* Lower Shin */}
            <path
              d="M 28 95 Q 32 135 36 160"
              fill="none"
              stroke={INK_CHARCOAL}
              strokeWidth="22"
              strokeLinecap="round"
            />
            <path
              d="M 28 95 Q 32 135 36 160"
              fill="none"
              stroke={PAPER_CREAM}
              strokeWidth="13"
              strokeLinecap="round"
            />

            {/* Chunky Illustrated Moon Boot */}
            <g transform="translate(18, 150)">
              <path
                d="M 5 10 L 25 10 Q 32 10 32 25 L 32 38 Q 32 45 22 45 L -8 45 Q -14 45 -14 36 L -10 24 Q -6 10 5 10 Z"
                fill={INK_CHARCOAL}
              />
              {/* Boot Sole Tread */}
              <rect x="-14" y="40" width="46" height="8" rx="3" fill="#3D4552" />
              <line x1="-8" y1="44" x2="26" y2="44" stroke={WARM_GOLD} strokeWidth="2.5" />
            </g>
          </g>
        </g>

        {/* ========================================================================= */}
        {/* 4. TORSO & SUIT DETAILS (Handcrafted Editorial Silhouette)               */}
        {/* ========================================================================= */}
        <g transform={`translate(180, ${250 + breath})`} filter="url(#hand-drawn-shadow)">
          {/* Main Spacesuit Torso Block */}
          <path
            d="M -45 -55 Q -52 15 -42 65 Q 0 75 42 65 Q 52 15 45 -55 Q 0 -62 -45 -55 Z"
            fill={PAPER_CREAM}
            stroke={INK_CHARCOAL}
            strokeWidth="5.5"
            strokeLinejoin="round"
          />

          {/* Tailored Chest Seams */}
          <path d="M -30 -35 L 30 -35" stroke="#D0C6B5" strokeWidth="3" />
          <path d="M -35 10 L 35 10" stroke="#D0C6B5" strokeWidth="3" />

          {/* Chest Life-Support Control Pack (Hand-inked module) */}
          <rect
            x="-28"
            y="-22"
            width="56"
            height="50"
            rx="10"
            fill="#E2D9CC"
            stroke={INK_CHARCOAL}
            strokeWidth="4"
          />

          {/* Circular Oxygen Level Indicator Needle */}
          <circle cx="-10" cy="3" r="12" fill={INK_CHARCOAL} />
          <circle cx="-10" cy="3" r="10" fill="#2C3542" />
          {/* Dial hand showing oxygen status */}
          <line
            x1="-10"
            y1="3"
            x2={pose === "panic_o2" ? "-17" : "-6"}
            y2={pose === "panic_o2" ? "7" : "-4"}
            stroke={pose === "panic_o2" ? DUSTY_CORAL : SAGE_GREEN}
            strokeWidth="3"
            strokeLinecap="round"
          />

          {/* Emergency Alert LED (Blinks on panic_o2) */}
          <circle
            cx="14"
            cy="-5"
            r="6"
            fill={pose === "panic_o2" && frame % 10 < 5 ? DUSTY_CORAL : SAGE_GREEN}
            stroke={INK_CHARCOAL}
            strokeWidth="2.5"
          />

          {/* Expedition Mission Patch (Warm Gold Triangle) */}
          <polygon
            points="14,10 8,24 20,24"
            fill={WARM_GOLD}
            stroke={INK_CHARCOAL}
            strokeWidth="2.5"
          />
        </g>

        {/* ========================================================================= */}
        {/* 5. FRONT ARM (Dynamic Poses: Telescope, Tablet, Pointing, Panic)         */}
        {/* ========================================================================= */}
        <g transform={`translate(205, ${210 + breath})`}>
          {/* Pose: WALK_EXPLORE */}
          {pose === "walk_explore" && (
            <g transform={`rotate(${armFront}, 0, 0)`}>
              <path
                d="M 0 0 Q 30 45 42 85"
                fill="none"
                stroke={INK_CHARCOAL}
                strokeWidth="20"
                strokeLinecap="round"
              />
              <path
                d="M 0 0 Q 30 45 42 85"
                fill="none"
                stroke={PAPER_CREAM}
                strokeWidth="12"
                strokeLinecap="round"
              />
              <circle cx="25" cy="40" r="12" fill="none" stroke={INK_CHARCOAL} strokeWidth="3" />
              {/* Hand holding portable scientific scanner */}
              <ellipse cx="44" cy="90" rx="15" ry="13" fill={INK_CHARCOAL} />
              {/* Mini Antenna */}
              <line x1="44" y1="90" x2="65" y2="75" stroke={INK_CHARCOAL} strokeWidth="4" />
              <circle cx="67" cy="73" r="4" fill={WARM_GOLD} />
            </g>
          )}

          {/* Pose: LOW_GRAVITY_JUMP (Arms outstretched for buoyant balance) */}
          {pose === "low_gravity_jump" && (
            <g transform="rotate(-35, 0, 0)">
              <path
                d="M 0 0 Q 40 30 75 35"
                fill="none"
                stroke={INK_CHARCOAL}
                strokeWidth="20"
                strokeLinecap="round"
              />
              <path
                d="M 0 0 Q 40 30 75 35"
                fill="none"
                stroke={PAPER_CREAM}
                strokeWidth="12"
                strokeLinecap="round"
              />
              <ellipse cx="80" cy="36" rx="14" ry="13" fill={INK_CHARCOAL} />
            </g>
          )}

          {/* Pose: CHECK_TELEMETRY (Holding holographic wrist PDA) */}
          {pose === "check_telemetry" && (
            <g transform="rotate(45, 0, 0)">
              <path
                d="M 0 0 Q 35 25 15 65"
                fill="none"
                stroke={INK_CHARCOAL}
                strokeWidth="20"
                strokeLinecap="round"
              />
              <path
                d="M 0 0 Q 35 25 15 65"
                fill="none"
                stroke={PAPER_CREAM}
                strokeWidth="12"
                strokeLinecap="round"
              />
              {/* Wrist Instrument Screen */}
              <rect x="0" y="55" width="30" height="20" rx="4" fill={INK_CHARCOAL} />
              <rect x="3" y="58" width="24" height="14" rx="2" fill={MUTED_BLUE} />
              <ellipse cx="15" cy="78" rx="14" ry="13" fill={INK_CHARCOAL} />
            </g>
          )}

          {/* Pose: ENTER_AIRLOCK (Reaching out toward habitat airlock door) */}
          {pose === "enter_airlock" && (
            <g transform="rotate(-15, 0, 0)">
              <path
                d="M 0 0 Q 45 20 85 20"
                fill="none"
                stroke={INK_CHARCOAL}
                strokeWidth="20"
                strokeLinecap="round"
              />
              <path
                d="M 0 0 Q 45 20 85 20"
                fill="none"
                stroke={PAPER_CREAM}
                strokeWidth="12"
                strokeLinecap="round"
              />
              <ellipse cx="90" cy="20" rx="15" ry="13" fill={INK_CHARCOAL} />
            </g>
          )}

          {/* Pose: PANIC_O2 (Both hands clutching chest / throat) */}
          {pose === "panic_o2" && (
            <g transform="rotate(40, 0, 0)">
              <path
                d="M 0 0 Q 20 30 -15 35"
                fill="none"
                stroke={INK_CHARCOAL}
                strokeWidth="20"
                strokeLinecap="round"
              />
              <path
                d="M 0 0 Q 20 30 -15 35"
                fill="none"
                stroke={PAPER_CREAM}
                strokeWidth="12"
                strokeLinecap="round"
              />
              <ellipse cx="-18" cy="35" rx="15" ry="13" fill={INK_CHARCOAL} />
            </g>
          )}

          {/* Pose: POINT_SKY (Directing viewer attention to Options A vs B) */}
          {pose === "point_sky" && (
            <g transform="rotate(-65, 0, 0)">
              <path
                d="M 0 0 Q 30 15 75 10"
                fill="none"
                stroke={INK_CHARCOAL}
                strokeWidth="20"
                strokeLinecap="round"
              />
              <path
                d="M 0 0 Q 30 15 75 10"
                fill="none"
                stroke={PAPER_CREAM}
                strokeWidth="12"
                strokeLinecap="round"
              />
              <ellipse cx="80" cy="10" rx="15" ry="13" fill={INK_CHARCOAL} />
              {/* Extended pointing finger */}
              <line x1="85" y1="10" x2="105" y2="5" stroke={INK_CHARCOAL} strokeWidth="6" strokeLinecap="round" />
            </g>
          )}
        </g>

        {/* ========================================================================= */}
        {/* 6. ASTRONAUT HEAD & DISTINCTIVE HELMET (Handcrafted Mascot Face)         */}
        {/* ========================================================================= */}
        <g transform={`translate(180, ${125 + breath})`} filter="url(#hand-drawn-shadow)">
          {/* Neck Collar Ring */}
          <ellipse
            cx="0"
            cy="52"
            rx="46"
            ry="14"
            fill="#D0C6B5"
            stroke={INK_CHARCOAL}
            strokeWidth="5"
          />

          {/* Outer Helmet Sphere (Friendly, slightly oversized chibi mascot proportions) */}
          <circle
            cx="0"
            cy="0"
            r="65"
            fill={PAPER_CREAM}
            stroke={INK_CHARCOAL}
            strokeWidth="6"
          />

          {/* Distinctive Sleek Bubble Visor (Clean reflective shield - no facial cartoon features) */}
          <ellipse
            cx="14"
            cy="2"
            rx="44"
            ry="36"
            fill="url(#editorial-visor)"
            stroke={INK_CHARCOAL}
            strokeWidth="4.5"
          />

          {/* Visor Sunlight Highlight Crescent & Specular Reflections */}
          <path
            d="M -15 -20 Q 14 -32 40 -12 Q 18 -22 -15 -20 Z"
            fill="url(#visor-glint)"
            transform={`translate(${visorShimmer * 0.4}, 0)`}
          />
          <path
            d="M -8 -8 Q 18 -16 38 4"
            fill="none"
            stroke="rgba(255, 255, 255, 0.45)"
            strokeWidth="3.5"
            strokeLinecap="round"
          />
          <ellipse cx="28" cy="-6" rx="6" ry="3" fill="rgba(255, 255, 255, 0.6)" transform="rotate(-20 28 -6)" />

          {/* Helmet Radio Antenna with Brass Warm Gold Tip */}
          <line x1="-45" y1="-25" x2="-68" y2="-65" stroke={INK_CHARCOAL} strokeWidth="4.5" strokeLinecap="round" />
          <circle cx="-70" cy="-68" r="5.5" fill={WARM_GOLD} stroke={INK_CHARCOAL} strokeWidth="3" />
        </g>
      </svg>
    </div>
  );
};
