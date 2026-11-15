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
import { CinematicEnvironment } from "./components/CinematicEnvironment";
import { IllustratedCharacter } from "./components/IllustratedCharacter";
import { InWorldHUD } from "./components/InWorldHUD";
import { InfographicDocumentary } from "./components/InfographicDocumentary";
import { KineticSubtitles } from "./components/KineticSubtitles";

export const AnimatedShort: React.FC<ProjectData> = ({
  scenes = [],
  words = [],
  audio_url,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentTime = frame / fps;

  // Find active scene
  let activeScene = scenes[0];
  let activeSceneIndex = 0;
  for (let i = 0; i < scenes.length; i++) {
    if (currentTime >= scenes[i].start_time && currentTime < scenes[i].end_time) {
      activeScene = scenes[i];
      activeSceneIndex = i;
      break;
    }
  }

  // Calculate local scene frame
  const sceneStartFrame = Math.round(activeScene.start_time * fps);
  const sceneDurationFrames = Math.max(
    15,
    Math.round(activeScene.duration * fps)
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0D0E12",
        overflow: "hidden",
        width: 1080,
        height: 1920,
      }}
    >
      {/* --- MASTER AUDIO TRACK --- */}
      {audio_url && <Audio src={staticFile(audio_url)} />}

      {/* --- SCENE VISUALS --- */}
      {scenes.map((scene, idx) => {
        const startFrame = Math.round(scene.start_time * fps);
        const durationFrames = Math.max(
          15,
          Math.round(scene.duration * fps)
        );

        return (
          <Sequence
            key={scene.scene_id}
            from={startFrame}
            durationInFrames={durationFrames}
          >
            {scene.is_infographic ? (
              /* Infographic Documentary Screen */
              <InfographicDocumentary
                spec={scene.infographic_spec}
                durationInFrames={durationFrames}
              />
            ) : (
              /* Cinematic Illustrated 2D Scene with Camera Rig */
              <CameraRig
                cameraType={scene.camera}
                durationInFrames={durationFrames}
              >
                {/* 1. Multi-Layer Environment */}
                <CinematicEnvironment
                  environment={scene.environment}
                  lighting={scene.lighting}
                />

                {/* 2. Persistent Protagonist Character */}
                <IllustratedCharacter
                  expression={scene.character_expression}
                  pose={scene.character_pose}
                  x={
                    scene.environment === "street_curbside"
                      ? 0.72
                      : scene.environment === "bank_counter"
                      ? 0.42
                      : 0.5
                  }
                  y={0.62}
                  scale={scene.camera === "snap_zoom" ? 1.25 : 1.05}
                />
              </CameraRig>
            )}
          </Sequence>
        );
      })}

      {/* --- IN-WORLD HUD (Visible on all scenes where hud_state is provided) --- */}
      {activeScene && activeScene.hud_state && (
        <InWorldHUD state={activeScene.hud_state} />
      )}

      {/* --- BURNED-IN KINETIC SUBTITLES --- */}
      <KineticSubtitles words={words} />

      {/* --- GLOBAL CINEMATIC GRAIN & VIGNETTE OVERLAY --- */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          pointerEvents: "none",
          boxShadow: "inset 0 0 160px rgba(0, 0, 0, 0.8)",
          zIndex: 80,
        }}
      />
    </AbsoluteFill>
  );
};
