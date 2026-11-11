package com.visionflow.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class RedisResultListener {

    @Autowired
    private SimpMessagingTemplate messagingTemplate;

    public void handleMessage(String message) {
        log.debug("Received detection result from AI Engine: {}", message);
        // Forwarding directly to WebSockets
        messagingTemplate.convertAndSend("/topic/detections", message);
    }
}
