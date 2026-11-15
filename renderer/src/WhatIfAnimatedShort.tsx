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
import { SpaceCaptions } from "./components/space/SpaceCaptions";

/**
 * WHAT IF? — Version 2.1 Handcrafted 2D Animated Composition
 * - Diverse scene storytelling: Spacecraft, Planet Mars, Satellites, Rovers, Geodesic Dome, Dust Storm, Rocket Launch
 * - Clean reflective astronaut helmet visor (no cartoon face)
 * - Top HUD bar removed for clean cinematic framing
 * - High-contrast Black & White kinetic subtitles (elevated, auto-wrapping, non-AI typography)
 * - Standalone educational short without series/game cliffhangers
 */
export const WhatIfAnimatedShort: React.FC<ProjectData> = ({
  scenes = [],
  words = [],
  audio_url = "space_soundtrack.wav",
}) => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0D1117",
        overflow: "hidden",
        width: 1080,
        height: 1920,
        fontFamily:
          'Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
      }}
    >
      {/* --- MASTER AUDIO TRACK (Brian Narrator + Deep Space Tension Score + SFX) --- */}
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
              {/* 1. Multi-layered Handcrafted Space Environment with Spacecraft, Planet, Satellite, Rover, Rocket */}
              <SpaceEnvironment
                environment={scene.environment}
                planet="mars"
                sceneId={scene.scene_id}
              />

              {/* 2. Character Presence (Only where appropriate - not dominating every frame) */}
              {/* Scene 1: Orbit arrival - No astronaut on screen; Sun, Mars planet & Satellite take center stage */}

              {scene.scene_id === 2 && (
                /* Scene 2: Low-gravity leap across dunes in front of 3-story exploration lander */
                <AstronautStickman
                  pose="low_gravity_jump"
                  expression="alert"
                  x={0.62}
                  y={0.52}
                  scale={1.05}
                  facing="right"
                />
              )}

              {scene.scene_id === 3 && (
                /* Scene 3: Inspecting mineral core beside the autonomous science rover */
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
                /* Scene 4: Reaching Base Alpha airlock beside the solar panel fields */
                <AstronautStickman
                  pose="enter_airlock"
                  expression="relief"
                  x={0.28}
                  y={0.54}
                  scale={1.05}
                  facing="right"
                />
              )}

              {scene.scene_id === 5 && (
                /* Scene 5: Bracing against the howling 100 km/h dust storm */
                <AstronautStickman
                  pose="panic_o2"
                  expression="shock"
                  x={0.46}
                  y={0.52}
                  scale={1.15}
                  facing="right"
                />
              )}

              {scene.scene_id === 6 && (
                /* Scene 6: Looking up proudly as the Mars Ascent Vehicle rocket launches into space */
                <AstronautStickman
                  pose="point_sky"
                  expression="focused"
                  x={0.24}
                  y={0.68}
                  scale={0.75}
                  facing="right"
                />
              )}
            </CameraRig>
          </Sequence>
        );
      })}

      {/* --- KINETIC SUBTITLES (Black & White, elevated to bottom: 280px, zero overlap) --- */}
      <SpaceCaptions words={words} />

      {/* --- AUTHENTIC FULL-FRAME TACTILE PAPER GRAIN TEXTURE --- */}
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
          <feTurbulence
            type="fractalNoise"
            baseFrequency="0.65"
            numOctaves="4"
            stitchTiles="stitch"
          />
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
          boxShadow: "inset 0 0 100px rgba(10, 13, 18, 0.65)",
          zIndex: 90,
        }}
      />
    </AbsoluteFill>
  );
};
