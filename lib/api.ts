// lib/api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Helper: get auth headers (no crash if no token)
function authHeaders(json = false): Record<string, string> {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
  const headers: Record<string, string> = {};
  if (json) headers['Content-Type'] = 'application/json';
  if (token) headers['Authorization'] = `Bearer ${token}`;
  return headers;
}

export const api = {
  // --- Health ---
  async healthCheck() {
    const response = await fetch(`${API_URL}/health`);
    return response.json();
  },

  // --- Upload ---
  async uploadReferenceImages(files: File[]) {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));
    const response = await fetch(`${API_URL}/api/upload/reference-images`, {
      method: 'POST',
      headers: authHeaders(),
      body: formData,
    });
    return response.json();
  },

  // --- AI Analysis ---
  async analyzeMood(data: {
    text_description?: string;
    image_urls?: string[];
    budget_min?: number;
    budget_max?: number;
    location?: string;
  }) {
    const response = await fetch(`${API_URL}/api/analysis/mood`, {
      method: 'POST',
      headers: authHeaders(true),
      body: JSON.stringify(data),
    });
    return response.json();
  },

  // --- Matching — FIXED: URL and body now match backend ---
  async matchPhotographers(data: {
    text_description: string;
    budget_max?: number;
    city?: string;
    min_rating?: number;
    top_k?: number;
  }) {
    const response = await fetch(`${API_URL}/api/matching/match`, {
      method: 'POST',
      headers: authHeaders(true),
      body: JSON.stringify({ top_k: 10, ...data }),
    });
    return response.json();
  },

  // --- Photographers ---
  async getPhotographers(params?: Record<string, string | number>) {
    const queryParams = new URLSearchParams(
      Object.entries(params || {}).map(([k, v]) => [k, String(v)])
    );
    const response = await fetch(`${API_URL}/api/photographers?${queryParams}`);
    return response.json();
  },

  async getPhotographerById(buddyId: string) {
    const response = await fetch(`${API_URL}/api/photographers/${buddyId}`);
    return response.json();
  },

  // --- Auth ---
  async register(email: string, password: string, name: string) {
    const response = await fetch(`${API_URL}/api/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, name }),
    });
    return response.json();
  },

  async login(email: string, password: string) {
    const body = new URLSearchParams({ username: email, password });
    const response = await fetch(`${API_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: body.toString(),
    });
    const data = await response.json();
    if (data.access_token) {
      localStorage.setItem('token', data.access_token);
    }
    return data;
  },

  logout() {
    localStorage.removeItem('token');
  },

  isLoggedIn(): boolean {
    return typeof window !== 'undefined' && !!localStorage.getItem('token');
  },
};
