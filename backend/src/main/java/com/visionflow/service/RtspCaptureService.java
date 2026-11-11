package com.visionflow.service;

import jakarta.annotation.PostConstruct;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.context.ApplicationContext;

import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.util.Base64;

@Service
@Slf4j
public class RtspCaptureService {

    @Value("${rtsp.stream.url:rtsp://localhost:8554/stream}")
    private String rtspUrl;

    @Autowired
    private FramePublisher framePublisher;

    @Autowired
    private ApplicationContext applicationContext;

    private boolean running = true;

    @PostConstruct
    public void init() {
        // Use applicationContext to get the proxy for @Async to work
        RtspCaptureService self = applicationContext.getBean(RtspCaptureService.class);
        self.startCapture();
    }

    @Async
    public void startCapture() {
        log.info("Starting VisionFlow Ingestion Service...");
        log.info("Target RTSP Stream: {}", rtspUrl);

        while (running) {
            try {
                // High-performance simulation of a factory floor
                byte[] imageData = generateIndustrialFrame();

                // 1. Publish to Redis for AI Engine (GPU Inference)
                framePublisher.publishFrame("camera-1", imageData);

                // 2. Publish to WebSockets for Frontend Real-time view
                framePublisher.publishToWebsocket("camera-1", imageData);

                Thread.sleep(100); // 10 FPS
            } catch (Exception e) {
                log.error("Ingestion error", e);
            }
        }
    }

    private byte[] generateIndustrialFrame() throws Exception {
        int width = 640;
        int height = 360;
        BufferedImage image = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
        Graphics2D g2d = image.createGraphics();

        // Background - Factory Floor
        g2d.setColor(new Color(40, 40, 40));
        g2d.fillRect(0, 0, width, height);

        // Conveyor Belt
        g2d.setColor(Color.BLACK);
        g2d.fillRect(0, 150, width, 100);

        // Moving Box
        g2d.setColor(new Color(139, 69, 19)); // Brown
        int boxX = (int) ((System.currentTimeMillis() / 10) % (width + 100)) - 50;
        g2d.fillRect(boxX, 160, 80, 80);

        // Simulated "Defect" on box
        if (boxX % 200 < 50) {
            g2d.setColor(Color.RED);
            g2d.fillOval(boxX + 20, 180, 10, 10);
        }

        g2d.dispose();

        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ImageIO.write(image, "jpg", baos);
        return baos.toByteArray();
    }

    public void stop() {
        this.running = false;
    }
}
