# VisionFlow AI

Real-time industrial inspection platform powered by YOLOv11 computer vision for Industry 4.0 manufacturing environments.

## Architecture

```
┌──────────┐     ┌────────────────┐     ┌─────────────┐     ┌──────────────┐
│  RTSP    │────>│   Backend      │────>│   Redis     │────>│  AI Engine   │
│  Camera  │     │  (Spring Boot) │     │  (Pub/Sub)  │     │  (YOLOv11)   │
└──────────┘     └───────┬────────┘     └──────┬──────┘     └──────────────┘
                         │                     │
                    WebSocket            Results Channel
                         │                     │
                 ┌───────┴────────┐            │
                 │    Nginx       │<───────────┘
                 │ (Reverse Proxy)│
                 └───────┬────────┘
                         │
                 ┌───────┴────────┐
                 │   Frontend     │
                 │ (Canvas + STOMP)│
                 └────────────────┘
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Java 21, Spring Boot 3.4.3, JavaCV 1.5.11 |
| AI Engine | Python 3, YOLOv11 (ultralytics 8.3.40), CUDA 12.4 |
| Frontend | HTML5 Canvas, STOMP WebSocket, Tailwind CSS |
| Infrastructure | Docker, Redis 7.4, Nginx 1.27 |

## Prerequisites

- Docker & Docker Compose v2+
- NVIDIA GPU with CUDA support
- NVIDIA Container Toolkit

## Quick Start

```bash
# 1. Clone the repository
git clone <repository-url>
cd visionflow-ai

# 2. Configure environment
cp .env.example .env
# Edit .env with your passwords

# 3. Build and start
docker compose up --build

# 4. Open dashboard
# http://localhost:80
```

## Configuration

All configuration is managed via environment variables. See `.env.example` for all available options:

| Variable | Description | Default |
|----------|-------------|---------|
| `REDIS_PASSWORD` | Redis authentication password | `changeme` |
| `SECURITY_ADMIN_USERNAME` | Backend admin username | `admin` |
| `SECURITY_ADMIN_PASSWORD` | Backend admin password (bcrypt hash) | (default hash) |
| `WEBSOCKET_ALLOWED_ORIGINS` | Allowed WebSocket origins (comma-separated) | `http://localhost` |
| `RTSP_STREAM_URL` | RTSP camera stream URL | `rtsp://localhost:8554/stream` |

## Project Structure

```
visionflow-ai/
├── backend/                    # Spring Boot backend
│   ├── src/main/java/com/visionflow/
│   │   ├── config/            # Security, WebSocket, Redis configs
│   │   ├── service/           # Frame capture, publishing, result listener
│   │   └── VisionFlowApplication.java
│   ├── Dockerfile
│   └── pom.xml
├── ai-engine/                  # Python AI engine
│   ├── main.py                # Redis worker with input validation
│   ├── vision_processor.py    # YOLOv11 batch inference
│   ├── test_smoke.py          # Smoke test
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                   # Web dashboard
│   ├── index.html             # Dashboard with SRI-protected CDN
│   └── app.js                 # WebSocket client, canvas renderer
├── nginx/
│   └── nginx.conf             # Reverse proxy + security headers
├── docs/                       # Documentation
│   ├── SECURITY_REVIEW_REPORT.md
│   ├── VERSION_UPGRADE_REPORT.md
│   ├── DAST_PENTEST_GUIDE.md
│   ├── TUTORIAL.md
│   └── PRESENTATION.md
├── .github/workflows/
│   └── security.yml           # CI/CD security pipeline
├── docker-compose.yml
├── .env.example
└── .gitignore
```

## Security

This project implements the following security measures:

- **Authentication:** Spring Security with HTTP Basic + BCrypt
- **Authorization:** Role-based access control on API endpoints
- **Transport:** WSS support via Nginx reverse proxy
- **CORS:** Configurable WebSocket origin restrictions
- **Input Validation:** Frame size/dimension limits, payload schema validation
- **XSS Prevention:** DOM-based rendering (no innerHTML)
- **Security Headers:** CSP, X-Frame-Options, X-Content-Type-Options via Nginx
- **SRI:** Subresource Integrity on CDN scripts
- **Container Hardening:** Non-root users, network isolation, read-only mounts
- **CI/CD:** Automated SAST, dependency CVE scan, container scan, secret detection

See `docs/SECURITY_REVIEW_REPORT.md` for the full security assessment.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| GPU not detected | Install NVIDIA Container Toolkit: `apt install nvidia-container-toolkit` |
| Redis auth failure | Ensure `REDIS_PASSWORD` matches across all services in `.env` |
| WebSocket blocked | Add your domain to `WEBSOCKET_ALLOWED_ORIGINS` |
| 401 Unauthorized | Use correct credentials from `.env` |
| Build fails | Run `docker compose build --no-cache` |

## Documentation

- [Security Review Report](docs/SECURITY_REVIEW_REPORT.md)
- [Version Upgrade Report](docs/VERSION_UPGRADE_REPORT.md)
- [DAST & Penetration Testing Guide](docs/DAST_PENTEST_GUIDE.md)
- [Tutorial](docs/TUTORIAL.md)
- [Presentation](docs/PRESENTATION.md)

---

## 🛠️ Project Deep Dive & Technical Guide

### 🎯 Main Purpose
Real-time Computer Vision workflow automation and model inference pipeline.

### 🧰 Tecnologias Utilizadas (Tech Stack)
- **Primary Technologies:** Docker / Docker Compose, FastAPI, Java 21, Maven, Python 3.12, Spring Boot 3.4.3
- **Deployment Strategy:** Container-ready with standard Docker/Docker Compose integrations where applicable.

### 🚀 Como Implantar e Executar (How to Deploy & Run)
#### Backend (Java / Spring Boot)
1. Navigate to the backend directory.
2. Compile and run: `./mvnw spring-boot:run` or `mvn spring-boot:run`.

#### Python Engine / FastAPI
1. Install dependencies: `pip install -r requirements.txt`.
2. Run the server/script: `uvicorn main:app --reload` or `python main.py`.

---
