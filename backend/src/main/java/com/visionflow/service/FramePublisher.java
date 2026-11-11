package com.visionflow.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Service;

import java.util.Base64;
import java.util.HashMap;
import java.util.Map;

@Service
@Slf4j
public class FramePublisher {

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    @Autowired
    private SimpMessagingTemplate messagingTemplate;

    private static final String FRAME_TOPIC = "visionflow:frames";

    public void publishFrame(String cameraId, byte[] frameData) {
        Map<String, String> payload = new HashMap<>();
        payload.put("cameraId", cameraId);
        payload.put("timestamp", String.valueOf(System.currentTimeMillis()));
        payload.put("data", Base64.getEncoder().encodeToString(frameData));

        redisTemplate.convertAndSend(FRAME_TOPIC, payload);
    }

    public void publishToWebsocket(String cameraId, byte[] frameData) {
        Map<String, String> payload = new HashMap<>();
        payload.put("cameraId", cameraId);
        payload.put("base64", Base64.getEncoder().encodeToString(frameData));

        messagingTemplate.convertAndSend("/topic/frames", payload);
    }
}
