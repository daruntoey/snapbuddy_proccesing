# SnapBuddy

> AI-Powered Aesthetic Photography Matching Platform

SnapBuddy is a production-ready AI platform that matches users with photographers based on aesthetic preferences, using advanced computer vision, NLP, and vector similarity matching.

## 🎯 Overview

SnapBuddy converts user aesthetic intent into real-world photoshoot outcomes by:

- **Analyzing** reference images using computer vision (CLIP embeddings)
- **Understanding** mood and style preferences via NLP
- **Matching** users with photographers using vector similarity
- **Ranking** recommendations with multi-factor scoring
- **Explaining** matches using AI-generated insights (Gemini API)

## 🏗️ Architecture

```
User Input → CV Analysis → Embedding Extraction → NLP Mood Understanding
    ↓
Unified Aesthetic Spec → Similarity Matching → Recommendation Ranking
    ↓
Satisfaction Prediction → AI Explanation → Final Recommendations
```

### Tech Stack

**Frontend**
- Next.js 14 (App Router)
- TypeScript
- TailwindCSS
- ShadCN UI

**Backend**
- FastAPI (Python 3.11)
- PostgreSQL
- Qdrant (Vector Database)
- Redis (Queue/Cache)

**AI Services**
- Google Gemini API (LLM)
- CLIP/OpenCLIP (Image Embeddings)
- Sentence Transformers (Text Embeddings)

**Cloud & Deployment**
- Google Cloud Storage
- Google Maps API
- Render (Hosting)
- Docker

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Google Cloud Account
- Render Account

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/snapbuddy.git
cd snapbuddy
```

2. **Set up environment variables**
```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env with your credentials

# Frontend
cp frontend/.env.example frontend/.env.local
# Edit frontend/.env.local with API URL
```

3. **Run with Docker Compose**
```bash
docker-compose up -d
```

4. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Qdrant Dashboard: http://localhost:6333/dashboard

### Manual Setup (Without Docker)

**Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

## 📊 Database Setup

The application uses PostgreSQL with vector support via pgvector extension.

```bash
# Migrations will run automatically on first startup
# Or manually:
cd backend
alembic upgrade head
```

## 🔑 Environment Variables

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/snapbuddy

# Google Cloud
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
GCS_BUCKET_NAME=snapbuddy-uploads

# Gemini API
GEMINI_API_KEY=your-gemini-api-key

# Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333

# Redis
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET=your-secret-key-change-this
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google Maps
GOOGLE_MAPS_API_KEY=your-maps-api-key
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your-maps-api-key
```

## 📚 API Documentation

Access interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

See [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) for detailed endpoint information.

## 🚢 Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions for:
- Render
- Google Cloud
- Docker containers

### Quick Deploy to Render

1. Push code to GitHub
2. Connect repository to Render
3. Render will auto-detect `render.yaml`
4. Set environment variables in Render dashboard
5. Deploy!

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# E2E tests
npm run test:e2e
```

## 📁 Project Structure

```
snapbuddy/
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── ai/       # AI services (CV, NLP, Gemini)
│   │   ├── api/      # API routes
│   │   ├── models/   # SQLAlchemy models
│   │   ├── schemas/  # Pydantic schemas
│   │   ├── services/ # Business logic
│   │   └── repositories/ # Data access layer
│   └── requirements.txt
├── frontend/          # Next.js application
│   ├── src/
│   │   ├── app/      # App router pages
│   │   ├── components/ # React components
│   │   └── lib/      # Utilities
│   └── package.json
└── docker-compose.yml
```

## 🎨 Features

- ✅ **Image Upload & Analysis**: Upload reference images, extract aesthetic features
- ✅ **Mood Input**: Describe desired photography style in natural language
- ✅ **AI Matching**: Vector similarity matching with photographer portfolios
- ✅ **Smart Ranking**: Multi-factor scoring (style, budget, location, availability)
- ✅ **AI Explanations**: Natural language explanations of match reasoning
- ✅ **Photographer Profiles**: View portfolios, ratings, and availability
- ✅ **Booking System**: Schedule photoshoots with matched photographers
- ✅ **Dashboard**: Track bookings, view history, manage preferences

## 🤖 AI Pipeline

1. **Computer Vision Service**: Extract CLIP embeddings from reference images
2. **NLP Mood Analyzer**: Convert text descriptions to aesthetic vectors
3. **Aesthetic Spec Engine**: Merge visual + textual features
4. **Matching Engine**: Vector similarity search in Qdrant
5. **Ranking Engine**: Score based on style, performance, budget, location
6. **Satisfaction Predictor**: ML-based success probability
7. **Explanation Generator**: Gemini-powered natural language reasoning

## 📈 Matching Formula

```
Final Score = (0.40 × Style Similarity) + 
              (0.25 × Historical Performance) + 
              (0.15 × Budget Fit) + 
              (0.10 × Availability) + 
              (0.10 × Distance Match)
```

## 🛠️ Development

```bash
# Install pre-commit hooks
pre-commit install

# Run linters
cd backend && black . && isort .
cd frontend && npm run lint

# Format code
npm run format
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

## 🔗 Links

- [Documentation](./docs)
- [API Reference](./API_DOCUMENTATION.md)
- [Deployment Guide](./DEPLOYMENT.md)
- [Architecture Overview](./docs/ARCHITECTURE.md)

## 🆘 Support

- Issues: [GitHub Issues](https://github.com/yourusername/snapbuddy/issues)
- Email: support@snapbuddy.com
- Discord: [Join our community](https://discord.gg/snapbuddy)

---

Built with ❤️ using AI-first architecture
