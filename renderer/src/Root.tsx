import React from "react";
import { Composition } from "remotion";
import { AnimatedShort } from "./AnimatedShort";
import { ProjectData } from "./types/schema";

const defaultProjectProps: ProjectData = {
  project_id: "default_preview",
  topic: "The $300,000 Government Coin Glitch",
  total_duration: 60.0,
  character_bible: {
    character_id: "hero_arbitrageur",
    name: "Felix",
    silhouette: "Dark cap and oversized hoodie",
    face_shape: "Rounded light face",
    face_color: "#F8F6F2",
    headwear: "Charcoal cap",
    clothing: "Charcoal hoodie with pink drawstrings",
    legs_and_feet: "Black joggers and white sneakers",
    expression_library: ["scheming_smirk", "focused_typing", "wide_shock", "triumphant"],
    body_animations: ["typing", "wheeling_cart", "box_lifting"],
  },
  scenes: [
    {
      scene_id: 1,
      beat: "HOOK",
      duration: 3.5,
      start_time: 0.0,
      end_time: 3.5,
      narration: "He ordered 300,000 dollars in government coins... and the shipping was completely free.",
      visual_description: "Dim hallway with gold crates",
      character_action: "Holding coin",
      environment: "dim_apartment_hallway",
      camera: "slow_push_in",
      lighting: "dim_magenta_neon",
      character_expression: "scheming_smirk",
      character_pose: "holding_coin",
      hud_state: {
        label_1: "COINS",
        val_1: "$300,000",
        label_2: "SHIPPING",
        val_2: "$0.00",
        label_3: "RISK",
        val_3: "10%",
        progress_percent: 10,
      },
      music_state: "mystery",
      transition: "hard_cut",
    },
  ],
  words: [
    { word: "He", start: 0.1, end: 0.3 },
    { word: "ordered", start: 0.35, end: 0.7 },
    { word: "$300,000", start: 0.75, end: 1.3, is_emphasized: true },
    { word: "in", start: 1.35, end: 1.5 },
    { word: "government", start: 1.55, end: 1.9 },
    { word: "coins...", start: 1.95, end: 2.3, is_emphasized: true },
    { word: "and", start: 2.35, end: 2.5 },
    { word: "the", start: 2.55, end: 2.7 },
    { word: "shipping", start: 2.75, end: 3.0, is_emphasized: true },
    { word: "was", start: 3.05, end: 3.15 },
    { word: "free.", start: 3.2, end: 3.5, is_emphasized: true },
  ],
  audio_url: "soundtrack.wav",
};

import { WhatIfAnimatedShort } from "./WhatIfAnimatedShort";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="WhatIfShort"
        component={WhatIfAnimatedShort as any}
        durationInFrames={1500}
        calculateMetadata={({ props }) => {
          const p = props as any;
          const lastScene = p?.scenes && p.scenes.length > 0 ? p.scenes[p.scenes.length - 1] : null;
          const totalDur = lastScene?.end_time || p?.total_duration || 50.0;
          const totalFrames = Math.max(900, Math.round(totalDur * 30));
          return {
            durationInFrames: totalFrames,
          };
        }}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={defaultProjectProps}
      />
      <Composition
        id="CinematicShort"
        component={AnimatedShort as any}
        durationInFrames={1800}
        calculateMetadata={({ props }) => {
          const totalDur = (props as any)?.total_duration || 60;
          const totalFrames = Math.max(1800, Math.round(totalDur * 30) + 30);
          return {
            durationInFrames: totalFrames,
          };
        }}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={defaultProjectProps}
      />
    </>
  );
};
