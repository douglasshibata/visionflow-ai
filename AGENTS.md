# AGENTS.md

Este arquivo fornece instruções e contexto para agentes de IA que trabalham no projeto **VisionFlow AI**.

## Visão Geral do Projeto
Plataforma de inspeção industrial em tempo real baseada em visão computacional (YOLOv11) para ambientes de manufatura Industry 4.0.

## Tecnologias Utilizadas
- **Backend:** Java 21, Spring Boot 3.4.3, JavaCV.
- **AI Engine:** Python 3, YOLOv11 (ultralytics), CUDA 12.4.
- **Mensageria:** Redis (Pub/Sub).
- **Frontend:** HTML5 Canvas, STOMP WebSocket, Tailwind CSS.
- **Infraestrutura:** Docker, Nginx.

## Estrutura de Pastas
- `backend/`: Backend Spring Boot.
- `ai-engine/`: Motor de processamento YOLO.
- `frontend/`: Dashboard web.
- `nginx/`: Proxy reverso e segurança.

## Comandos Principais
- Build/Instalação: `docker compose up --build`
- Testes: `python ai-engine/test_smoke.py`
- Execução Backend: `./mvnw spring-boot:run`

## Diretrizes de Desenvolvimento
- **Baixa Latência:** Otimize a comunicação Redis Pub/Sub e WebSockets.
- **Segurança:** Autenticação HTTP Basic + BCrypt, SRI em scripts, e hardening de containers (não-root).
- **Validação:** Verifique dimensões de frames para evitar ataques de DoS/estouro de memória.
- **GPU:** Requer NVIDIA Container Toolkit para processamento YOLO.
