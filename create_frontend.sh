#!/bin/bash

mkdir -p frontend/src/{app,components,lib,types,styles}
mkdir -p frontend/public

# Create package.json
cat > frontend/package.json << 'EOF'
{
  "name": "snapbuddy-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "14.1.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-dropdown-menu": "^2.0.6",
    "@radix-ui/react-slot": "^1.0.2",
    "@radix-ui/react-tabs": "^1.0.4",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "lucide-react": "^0.309.0",
    "tailwind-merge": "^2.2.0",
    "tailwindcss-animate": "^1.0.7",
    "axios": "^1.6.5",
    "framer-motion": "^10.18.0",
    "react-dropzone": "^14.2.3"
  },
  "devDependencies": {
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "autoprefixer": "^10.0.1",
    "postcss": "^8",
    "tailwindcss": "^3.3.0",
    "typescript": "^5"
  }
}
EOF

# Create tsconfig.json
cat > frontend/tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
EOF

# Create next.config.js
cat > frontend/next.config.js << 'EOF'
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['storage.googleapis.com'],
  },
}

module.exports = nextConfig
EOF

# Create tailwind.config.ts
cat > frontend/tailwind.config.ts << 'EOF'
import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};
export default config;
EOF

# Create globals.css
cat > frontend/src/app/globals.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 221.2 83.2% 53.3%;
  }
}
EOF

# Create layout.tsx
cat > frontend/src/app/layout.tsx << 'EOF'
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "SnapBuddy - AI Photography Matching",
  description: "Find your perfect photographer with AI-powered aesthetic matching",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
EOF

# Create homepage
cat > frontend/src/app/page.tsx << 'EOF'
import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-6xl font-bold mb-6 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            SnapBuddy
          </h1>
          <p className="text-2xl text-gray-700 mb-8">
            Find Your Perfect Photographer with AI
          </p>
          <p className="text-lg text-gray-600 mb-12">
            Upload your aesthetic inspiration, describe your vision, and let our AI match you with photographers who truly get your vibe.
          </p>
          
          <div className="flex gap-4 justify-center">
            <Link
              href="/upload"
              className="px-8 py-4 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition"
            >
              Start Matching
            </Link>
            <Link
              href="/photographers"
              className="px-8 py-4 bg-white text-blue-600 rounded-lg font-semibold border-2 border-blue-600 hover:bg-blue-50 transition"
            >
              Browse Photographers
            </Link>
          </div>

          <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-xl shadow-lg">
              <div className="text-4xl mb-4">📸</div>
              <h3 className="text-xl font-bold mb-2">Upload Inspiration</h3>
              <p className="text-gray-600">Share reference images that capture your desired aesthetic</p>
            </div>
            
            <div className="bg-white p-6 rounded-xl shadow-lg">
              <div className="text-4xl mb-4">🤖</div>
              <h3 className="text-xl font-bold mb-2">AI Matching</h3>
              <p className="text-gray-600">Our AI analyzes your style and matches you with perfect photographers</p>
            </div>
            
            <div className="bg-white p-6 rounded-xl shadow-lg">
              <div className="text-4xl mb-4">✨</div>
              <h3 className="text-xl font-bold mb-2">Book Your Shoot</h3>
              <p className="text-gray-600">Connect with your match and create stunning photos together</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
EOF

# Create upload page
cat > frontend/src/app/upload/page.tsx << 'EOF'
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function UploadPage() {
  const [description, setDescription] = useState("");
  const [files, setFiles] = useState<File[]>([]);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // Handle upload and analysis
    console.log("Analyzing...", { description, files });
    router.push("/results");
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12">
      <div className="container mx-auto px-4 max-w-3xl">
        <h1 className="text-4xl font-bold mb-8 text-center">Describe Your Vision</h1>
        
        <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-lg p-8">
          <div className="mb-6">
            <label className="block text-lg font-semibold mb-2">
              What aesthetic are you looking for?
            </label>
            <textarea
              className="w-full p-4 border rounded-lg h-32"
              placeholder="E.g., Cozy Korean cafe aesthetic with warm natural lighting and minimal poses..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>

          <div className="mb-6">
            <label className="block text-lg font-semibold mb-2">
              Upload Reference Images
            </label>
            <div className="border-2 border-dashed rounded-lg p-12 text-center">
              <input
                type="file"
                multiple
                accept="image/*"
                onChange={(e) => setFiles(Array.from(e.target.files || []))}
                className="hidden"
                id="file-upload"
              />
              <label htmlFor="file-upload" className="cursor-pointer">
                <div className="text-4xl mb-2">📷</div>
                <p className="text-gray-600">Click to upload images</p>
                <p className="text-sm text-gray-400">Up to 5 images</p>
              </label>
              {files.length > 0 && (
                <p className="mt-4 text-sm text-gray-600">{files.length} files selected</p>
              )}
            </div>
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-4 rounded-lg font-semibold hover:bg-blue-700 transition"
          >
            Find My Photographers
          </button>
        </form>
      </div>
    </main>
  );
}
EOF

# Create results page
cat > frontend/src/app/results/page.tsx << 'EOF'
"use client";

export default function ResultsPage() {
  const mockMatches = [
    {
      id: 1,
      name: "Studio Seoul",
      score: 95,
      image: "/placeholder.jpg",
      rate: "$150/hr",
      rating: 4.9,
      location: "Seoul",
    },
  ];

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12">
      <div className="container mx-auto px-4 max-w-6xl">
        <h1 className="text-4xl font-bold mb-8 text-center">Your Perfect Matches</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {mockMatches.map((match) => (
            <div key={match.id} className="bg-white rounded-xl shadow-lg overflow-hidden">
              <div className="h-48 bg-gray-200"></div>
              <div className="p-6">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-xl font-bold">{match.name}</h3>
                  <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-semibold">
                    {match.score}% Match
                  </span>
                </div>
                <p className="text-gray-600 mb-2">{match.location}</p>
                <p className="text-gray-800 font-semibold mb-4">{match.rate}</p>
                <button className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700">
                  View Profile
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
EOF

# Create photographers page
cat > frontend/src/app/photographers/page.tsx << 'EOF'
"use client";

export default function PhotographersPage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12">
      <div className="container mx-auto px-4">
        <h1 className="text-4xl font-bold mb-8 text-center">Browse Photographers</h1>
        <p className="text-center text-gray-600">Coming soon...</p>
      </div>
    </main>
  );
}
EOF

# Create API client
cat > frontend/src/lib/api.ts << 'EOF'
import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const uploadService = {
  uploadImages: async (files: File[]) => {
    const formData = new FormData();
    files.forEach(file => formData.append("files", file));
    return api.post("/api/upload/reference-images", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export const analysisService = {
  analyzeMood: async (data: any) => {
    return api.post("/api/analysis/mood", data);
  },
};

export const matchingService = {
  matchPhotographers: async (moodSpecId: number) => {
    return api.post("/api/matching/match-photographers", { mood_spec_id: moodSpecId });
  },
};
EOF

# Create types
cat > frontend/src/types/index.ts << 'EOF'
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
EOF

# Create .env.example
cat > frontend/.env.example << 'EOF'
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your-maps-api-key
EOF

# Create Dockerfile
cat > frontend/Dockerfile << 'EOF'
FROM node:18-alpine AS base

# Development stage
FROM base AS development
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]

# Builder stage
FROM base AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM base AS production
WORKDIR /app
ENV NODE_ENV production
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT 3000
CMD ["node", "server.js"]
EOF

echo "Frontend created successfully!"
