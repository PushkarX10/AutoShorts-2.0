export interface HudStateData {
  label_1: string;
  val_1: string;
  label_2: string;
  val_2: string;
  label_3: string;
  val_3: string;
  progress_percent: number;
}

export interface InfographicItem {
  label: string;
  val: string;
}

export interface InfographicSpecData {
  title: string;
  subtitle: string;
  threshold_label?: string;
  threshold_value?: string;
  breakdown_items: InfographicItem[];
  pink_highlight_stat: string;
  chart_type: string;
}

export interface SubtitleWordData {
  word: string;
  start: number;
  end: number;
  is_emphasized?: boolean;
}

export interface SceneData {
  scene_id: number;
  beat: string;
  duration: number;
  start_time: number;
  end_time: number;
  narration: string;
  visual_description: string;
  character_action: string;
  environment: string;
  camera: string;
  lighting: string;
  character_expression: string;
  character_pose: string;
  hud_state?: HudStateData;
  is_infographic?: boolean;
  infographic_spec?: InfographicSpecData;
  sound_effect?: string;
  music_state: string;
  transition: string;
  emphasized_words?: string[];
}

export interface CharacterBibleData {
  character_id: string;
  name: string;
  silhouette: string;
  face_shape: string;
  face_color: string;
  headwear: string;
  clothing: string;
  legs_and_feet: string;
  expression_library: string[];
  body_animations: string[];
}

export interface ProjectData {
  project_id: string;
  topic: string;
  total_duration: number;
  scenes: SceneData[];
  words: SubtitleWordData[];
  character_bible: CharacterBibleData;
  audio_url?: string;
}
