// lib/api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = {
  // ✅ ที่มีอยู่แล้ว
  async healthCheck() {
    const response = await fetch(`${API_URL}/health`);
    return response.json();
  },

  async uploadReferenceImages(files: File[]) {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));

    const response = await fetch(`${API_URL}/api/upload/reference-images`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
      body: formData,
    });

    return response.json();
  },

  // ⭐ เพิ่มใหม่ - AI Features
  async analyzeMood(data: {
    text_description?: string;
    image_urls?: string[];
    budget_min?: number;
    budget_max?: number;
    location?: string;
  }) {
    const response = await fetch(`${API_URL}/api/analysis/mood`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
      body: JSON.stringify(data),
    });
    return response.json();
  },

  async matchPhotographers(moodSpecId: number, limit: number = 10) {
    const response = await fetch(`${API_URL}/api/matching/match-photographers`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
      body: JSON.stringify({ mood_spec_id: moodSpecId, limit }),
    });
    return response.json();
  },

  async getPhotographers(params?: any) {
    const queryParams = new URLSearchParams(params);
    const response = await fetch(`${API_URL}/api/photographers?${queryParams}`);
    return response.json();
  },
};
