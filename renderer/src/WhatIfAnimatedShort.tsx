import React from "react";
import {
  AbsoluteFill,
  Audio,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { ProjectData } from "./types/schema";
import { CameraRig } from "./components/CameraRig";
import { SpaceEnvironment } from "./components/space/SpaceEnvironment";
import { AstronautStickman } from "./components/space/AstronautStickman";
import { SpaceHUD } from "./components/space/SpaceHUD";
import { SpaceCaptions } from "./components/space/SpaceCaptions";

/**
 * WHAT IF? — Version 2.0 Premium Handcrafted 2D Animated Composition
 * - Editorial Science-Journal & Hand-Drawn 2D vector animation
 * - 25-40% Mascot character prominence in character-focused scenes
 * - Full-frame tactile Paper Grain texture overlay
 * - Editorial Mission Field-Log HUD & Zero text overlap kinetic subtitles
 */
export const WhatIfAnimatedShort: React.FC<ProjectData> = ({
  scenes = [],
  words = [],
  audio_url = "space_soundtrack.wav",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentTime = frame / fps;

  // Find active scene
  let activeScene = scenes[0];
  for (let i = 0; i < scenes.length; i++) {
    if (currentTime >= scenes[i].start_time && currentTime < scenes[i].end_time) {
      activeScene = scenes[i];
      break;
    }
  }

  // Parse HUD state from active scene
  const hudState = activeScene?.hud_state
    ? {
        planet: activeScene.hud_state.label_1 || "Mars",
        solDay: activeScene.hud_state.val_1 || "SOL 18",
        oxygenPercent: activeScene.hud_state.progress_percent ?? 88,
        temperature: activeScene.hud_state.val_2 || "-63°C",
        gravity: activeScene.hud_state.val_3 || "0.38g",
        pressure: "0.006 ATM",
        alertLevel: (activeScene.hud_state.progress_percent ?? 88) < 30 ? ("critical" as const) : ("normal" as const),
      }
    : undefined;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#1A2028",
        overflow: "hidden",
        width: 1080,
        height: 1920,
        fontFamily: "'Outfit', 'Montserrat', -apple-system, sans-serif",
      }}
    >
      {/* --- MASTER AUDIO TRACK (Edge-TTS Narrator + Deep Space Ambient Score + SFX) --- */}
      {audio_url && <Audio src={staticFile(audio_url)} />}

      {/* --- 9:16 VERTICAL SCENE SEQUENCES --- */}
      {scenes.map((scene) => {
        const startFrame = Math.round(scene.start_time * fps);
        const durationFrames = Math.max(15, Math.round(scene.duration * fps));

        return (
          <Sequence
            key={scene.scene_id}
            from={startFrame}
            durationInFrames={durationFrames}
          >
            <CameraRig
              cameraType={scene.camera}
              durationInFrames={durationFrames}
            >
              {/* 1. Multi-layered Handcrafted Editorial Space Environment */}
              <SpaceEnvironment
                environment={scene.environment}
                planet="mars"
                sceneId={scene.scene_id}
              />

              {/* 2. Consistent Recurring Illustrated Astronaut Mascot (25-40% frame height) */}
              {scene.scene_id === 1 && (
                /* Scene 1: Astronaut standing on Martian ridge with field scanner */
                <AstronautStickman
                  pose="walk_explore"
                  expression="curious"
                  x={0.50}
                  y={0.52}
                  scale={1.22}
                  facing="right"
                />
              )}

              {scene.scene_id === 2 && (
                /* Scene 2: Low gravity jump demonstrating 0.38g parabolic physics */
                <AstronautStickman
                  pose="low_gravity_jump"
                  expression="alert"
                  x={0.48}
                  y={0.48}
                  scale={1.20}
                  facing="right"
                />
              )}

              {scene.scene_id === 3 && (
                /* Scene 3: Observing the Editorial Science Journal Comparison Spread */
                <AstronautStickman
                  pose="check_telemetry"
                  expression="focused"
                  x={0.88}
                  y={0.54}
                  scale={0.78}
                  facing="left"
                />
              )}

              {scene.scene_id === 4 && (
                /* Scene 4: Reaching the Base Alpha geodesic habitat airlock */
                <AstronautStickman
                  pose="enter_airlock"
                  expression="relief"
                  x={0.34}
                  y={0.52}
                  scale={1.20}
                  facing="right"
                />
              )}

              {scene.scene_id === 5 && (
                /* Scene 5: Sol 18 violent dust storm strikes, low O2 alert */
                <AstronautStickman
                  pose="panic_o2"
                  expression="shock"
                  x={0.50}
                  y={0.52}
                  scale={1.25}
                  facing="right"
                />
              )}

              {scene.scene_id === 6 && (
                /* Scene 6: Interactive Choice [ A ] vs [ B ] pointing to audience */
                <AstronautStickman
                  pose="point_sky"
                  expression="focused"
                  x={0.50}
                  y={0.54}
                  scale={1.05}
                  facing="right"
                />
              )}
            </CameraRig>
          </Sequence>
        );
      })}

      {/* --- MISSION CONTROL EDITORIAL FIELD-LOG HEADER (Anchored at top: 70px) --- */}
      {hudState && <SpaceHUD state={hudState} />}

      {/* --- KINETIC SUBTITLES (Anchored at bottom: 110px with zero text overlap) --- */}
      <SpaceCaptions words={words} />

      {/* --- AUTHENTIC FULL-FRAME TACTILE PAPER GRAIN TEXTURE (Eliminates digital vector sterility) --- */}
      <svg
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          pointerEvents: "none",
          zIndex: 92,
          opacity: 0.08,
          mixBlendMode: "multiply",
        }}
      >
        <filter id="global-paper-texture">
          <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="4" stitchTiles="stitch" />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter="url(#global-paper-texture)" />
      </svg>

      {/* --- SUBTLE EDITORIAL VIGNETTE BORDER --- */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          pointerEvents: "none",
          boxShadow: "inset 0 0 100px rgba(26, 32, 40, 0.65)",
          zIndex: 90,
        }}
      />
    </AbsoluteFill>
  );
};
