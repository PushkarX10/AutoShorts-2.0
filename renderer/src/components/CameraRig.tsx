import React from "react";
import { interpolate, useCurrentFrame, spring } from "remotion";

interface CameraRigProps {
  cameraType: string;
  durationInFrames: number;
  children: React.ReactNode;
}

export const CameraRig: React.FC<CameraRigProps> = ({
  cameraType,
  durationInFrames,
  children,
}) => {
  const frame = useCurrentFrame();

  let scale = 1.0;
  let translateX = 0;
  let translateY = 0;
  let rotate = 0;

  switch (cameraType) {
    case "slow_push_in":
    case "push_in":
      scale = interpolate(frame, [0, durationInFrames], [1.0, 1.15], {
        extrapolateRight: "clamp",
      });
      translateY = interpolate(frame, [0, durationInFrames], [0, -25], {
        extrapolateRight: "clamp",
      });
      break;

    case "pull_out":
      scale = interpolate(frame, [0, durationInFrames], [1.18, 1.0], {
        extrapolateRight: "clamp",
      });
      translateY = interpolate(frame, [0, durationInFrames], [-30, 0], {
        extrapolateRight: "clamp",
      });
      break;

    case "pan_left":
      scale = 1.06;
      translateX = interpolate(frame, [0, durationInFrames], [80, -60], {
        extrapolateRight: "clamp",
      });
      break;

    case "tracking_shot":
      scale = 1.08;
      translateX = interpolate(frame, [0, durationInFrames], [-90, 70], {
        extrapolateRight: "clamp",
      });
      // subtle organic camera bob
      translateY = Math.sin(frame * 0.18) * 8;
      break;

    case "snap_zoom": {
      const zoomSpring = spring({
        frame,
        fps: 30,
        config: { damping: 12, stiffness: 180, mass: 0.6 },
      });
      scale = interpolate(zoomSpring, [0, 1], [1.0, 1.28]);
      translateY = interpolate(zoomSpring, [0, 1], [0, -60]);
      break;
    }

    case "micro_shake": {
      scale = 1.05;
      const shakeX = (Math.sin(frame * 1.8) * 12 + Math.cos(frame * 2.7) * 8) *
        interpolate(frame, [0, 15, durationInFrames], [1, 0.4, 0.2]);
      const shakeY = (Math.cos(frame * 1.5) * 10 + Math.sin(frame * 3.1) * 7) *
        interpolate(frame, [0, 15, durationInFrames], [1, 0.4, 0.2]);
      translateX = shakeX;
      translateY = shakeY;
      rotate = Math.sin(frame * 0.9) * 0.6;
      break;
    }

    default: // static wide with subtle organic film drift
      scale = interpolate(frame, [0, durationInFrames], [1.0, 1.03], {
        extrapolateRight: "clamp",
      });
      translateX = Math.sin(frame * 0.05) * 5;
      translateY = Math.cos(frame * 0.04) * 4;
      break;
  }

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        transform: `scale(${scale}) translate(${translateX}px, ${translateY}px) rotate(${rotate}deg)`,
        transformOrigin: "center center",
        willChange: "transform",
      }}
    >
      {children}
    </div>
  );
};
