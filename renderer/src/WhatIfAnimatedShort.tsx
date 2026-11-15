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
 * WHAT IF? — Version 2.2 Handcrafted 2D Animated Composition
 * - True cinematic storytelling: Zero PowerPoint slides, zero comparison tables, zero label boxes
 * - Animated elements: rotating radar, rock-drilling laser sparks, boiling vacuum chamber, rocket liftoff
 * - Clean visual hierarchy with zero text collisions
 * - High-contrast White & Black kinetic captions (heavy black stroke, zero bounding box clipping)
 */
export const WhatIfAnimatedShort: React.FC<ProjectData> = ({
  scenes = [],
  words = [],
  audio_url = "space_soundtrack.wav",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0A0D14",
        overflow: "hidden",
        width: 1080,
        height: 1920,
        fontFamily:
          'Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
      }}
    >
      {/* --- MASTER AUDIO TRACK (Brian Narrator + Ambient Tension Score) --- */}
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
              {/* Scene 1: Orbit arrival - No astronaut; Sun, Mars planet & Satellite take center stage */}

              {scene.scene_id === 2 && (() => {
                // Animate low-gravity parabolic jump across the Martian dunes
                // Arc starts near the lander, reaches high apex, and lands on dune crest
                const sceneProgress = (frame - startFrame) / Math.max(1, durationFrames);
                const cycle = Math.min(Math.max(sceneProgress * 1.3, 0), 1.0);
                const leapX = 0.44 + cycle * 0.36;
                const leapHeight = 4 * 0.16 * cycle * (1 - cycle);
                const leapY = 0.58 - leapHeight;
                return (
                  <AstronautStickman
                    pose="low_gravity_jump"
                    expression="alert"
                    x={leapX}
                    y={leapY}
                    scale={1.02}
                    facing="right"
                  />
                );
              })()}

              {scene.scene_id === 3 && (
                /* Scene 3: Inspecting rock core beside autonomous rover and boiling vacuum test */
                <AstronautStickman
                  pose="check_telemetry"
                  expression="focused"
                  x={0.78}
                  y={0.56}
                  scale={0.75}
                  facing="left"
                />
              )}

              {scene.scene_id === 4 && (
                /* Scene 4: Approaching Base Alpha airlock beside the solar panel fields */
                <AstronautStickman
                  pose="enter_airlock"
                  expression="relief"
                  x={0.34}
                  y={0.55}
                  scale={1.02}
                  facing="right"
                />
              )}

              {scene.scene_id === 5 && (
                /* Scene 5: Bracing against the howling 100 km/h dust storm */
                <AstronautStickman
                  pose="panic_o2"
                  expression="shock"
                  x={0.48}
                  y={0.54}
                  scale={1.12}
                  facing="right"
                />
              )}

              {/* Scene 6: Astronaut safely inside the ascending MAV rocket */}
            </CameraRig>
          </Sequence>
        );
      })}

      {/* --- KINETIC SUBTITLES (White & Black, elevated to bottom: 320px, zero clipping) --- */}
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
