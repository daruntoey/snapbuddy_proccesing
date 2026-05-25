// lib/api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = {
  // Health Check
  async healthCheck() {
    const response = await fetch(`${API_URL}/health`);
    return response.json();
  },

  // Upload Reference Images
  async uploadReferenceImages(files: File[]) {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));

    const response = await fetch(`${API_URL}/api/upload/reference-images`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`, // ถ้ามี auth
      },
      body: formData,
    });

    return response.json();
  },

 // ⭐ เพิ่มใหม่: AI Mood Analysis
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
    
    if (!response.ok) {
      throw new Error('Mood analysis failed');
    }
    
    return response.json();
  },

  // ⭐ เพิ่มใหม่: Match Photographers with AI
  async matchPhotographers(moodSpecId: number, limit: number = 10) {
    const response = await fetch(`${API_URL}/api/matching/match-photographers`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
      body: JSON.stringify({
        mood_spec_id: moodSpecId,
        limit: limit,
      }),
    });

    if (!response.ok) {
      throw new Error('Photographer matching failed');
    }

    return response.json();
  },

  // ⭐ เพิ่มใหม่: Get Photographers List
  async getPhotographers(params?: {
    skip?: number;
    limit?: number;
    style?: string;
    min_rating?: number;
  }) {
    const queryParams = new URLSearchParams();
    if (params?.skip) queryParams.append('skip', params.skip.toString());
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    if (params?.style) queryParams.append('style', params.style);
    
    const response = await fetch(
      `${API_URL}/api/photographers?${queryParams}`,
      {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      }
    );

    return response.json();
  },

  // ⭐ เพิ่มใหม่: Get Photographer Detail
  async getPhotographerById(photographerId: number) {
    const response = await fetch(
      `${API_URL}/api/photographers/${photographerId}`,
      {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      }
    );

    return response.json();
  },

  // ⭐ เพิ่มใหม่: Create Booking
  async createBooking(bookingData: {
    photographer_id: number;
    booking_date: string;
    booking_duration_hours: number;
    location: string;
    mood_spec_id?: number;
    special_requests?: string;
  }) {
    const response = await fetch(`${API_URL}/api/bookings`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
      body: JSON.stringify(bookingData),
    });

    return response.json();
  },
};
