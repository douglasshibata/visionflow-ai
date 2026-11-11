# SKILLS.md - VisionFlow AI

Diretrizes para evolução da plataforma de inspeção industrial.

## 🛡️ Auditoria de Segurança

1. **WebSocket Security:** Garanta que as origens permitidas em `WEBSOCKET_ALLOWED_ORIGINS` sejam estritas em produção.
2. **Input Validation:** Audite a validação de dimensões de frames no `main.py` para evitar ataques de estouro de memória no processador YOLO.
3. **Hardening de Container:** Verifique se as imagens Docker rodam com usuários não-root e se as permissões de volume são restritivas.

## 📈 Melhorias Sugeridas

1. **Inteligência:**
   - Implementar treinamento incremental para que novos defeitos possam ser aprendidos sem retraining completo.
   - Adicionar suporte a múltiplos fluxos RTSP simultâneos com load balancing.
2. **UX Industrial:**
   - Criar um painel de estatísticas de defeitos detectados por turno.
   - Adicionar alertas visuais e sonoros configuráveis no dashboard.
3. **Performance:**
   - Otimizar a inferência YOLO usando TensorRT para maximizar o throughput na GPU.

## 🤖 Papel do Claude

- **Computer Vision Expert:** Ajude a ajustar os hiperparâmetros de confiança do YOLO para reduzir falsos positivos em ambientes ruidosos.
- **Java Architect:** Expanda a configuração do Spring Security para suportar autenticação baseada em certificados (mTLS).
- **System Engineer:** Otimize a serialização de frames no Redis para minimizar a latência de ponta a ponta.
