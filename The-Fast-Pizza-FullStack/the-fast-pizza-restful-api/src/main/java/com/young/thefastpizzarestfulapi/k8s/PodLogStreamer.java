package com.young.thefastpizzarestfulapi.k8s;

/**
 * desc:
 *
 * @author Young.
 * @since 2024/5/24 23:49
 */

import io.kubernetes.client.openapi.ApiClient;
import io.kubernetes.client.openapi.ApiException;
import io.kubernetes.client.openapi.Configuration;
import io.kubernetes.client.openapi.apis.CoreV1Api;
import io.kubernetes.client.util.Config;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class PodLogStreamer {

    private ApiClient client;
    private CoreV1Api api;

    public PodLogStreamer() throws Exception {
        // 初始化 Kubernetes 客户端
        client = Config.defaultClient();
        Configuration.setDefaultApiClient(client);
        api = new CoreV1Api(client);
    }

    public void streamPodLogs(String namespace, String podName, WebSocketSession session) throws ApiException {
        // 调用 Kubernetes API 获取日志
        ProcessBuilder processBuilder = new ProcessBuilder("kubectl", "logs", "-f", podName, "-n", namespace);
        try {
            Process process = processBuilder.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));

            String line;
            while ((line = reader.readLine()) != null) {
                session.sendMessage(new TextMessage(line));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

