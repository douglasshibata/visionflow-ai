# VisionFlow AI - CLAUDE.md

Guia de comandos e diretrizes para o VisionFlow AI.

## Comandos de Build e Execução

### Docker Compose (Recomendado)
```bash
# Requer NVIDIA GPU + Container Toolkit
docker compose up --build
```

### Backend (Spring Boot)
```bash
cd visionflow-ai/backend
./mvnw spring-boot:run
```

### AI Engine (Python)
```bash
cd visionflow-ai/ai-engine
python main.py
```

## Diretrizes de Desenvolvimento

- **Visão Computacional:** Utiliza YOLOv11 para inspeção industrial em tempo real.
- **Mensageria:** Redis Pub/Sub para comunicação entre o backend e o motor de IA.
- **Streaming:** WebSockets (STOMP) para envio de resultados para o frontend.
- **Segurança:** Autenticação via HTTP Basic + BCrypt. SRI em scripts de CDN.
- **Arquitetura:** Foco em baixa latência e Industry 4.0.
