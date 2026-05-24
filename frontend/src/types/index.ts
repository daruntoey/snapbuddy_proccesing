export interface Photographer {
  id: number;
  business_name: string;
  bio?: string;
  location: string;
  hourly_rate: number;
  average_rating: number;
  profile_image?: string;
}

export interface PhotographerMatch extends Photographer {
  match_score: number;
  explanation: string;
}

export interface MoodAnalysis {
  mood_spec_id: number;
  mood_tags: string[];
  style_tags: string[];
  detected_intent: string;
  aesthetic_summary: string;
}
