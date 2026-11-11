package com.visionflow;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class VisionFlowApplication {
    public static void main(String[] args) {
        SpringApplication.run(VisionFlowApplication.class, args);
    }
}
