package com.young.thefastpizzarestfulapi.k8s;

/**
 * desc:
 *
 * @author Young.
 * @since 2024/5/24 23:56
 */
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketHandler;
import org.springframework.web.socket.WebSocketMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

public class PodLogWebSocketHandler extends TextWebSocketHandler {

    private PodLogStreamer podLogStreamer;

    public PodLogWebSocketHandler() throws Exception {
        podLogStreamer = new PodLogStreamer();
    }

    @Override
    public void handleTextMessage(WebSocketSession session, TextMessage message) throws Exception {
        // 从客户端消息中解析 namespace 和 podName
        String[] payload = message.getPayload().split(" ");
        String namespace = payload[0];
        String podName = payload[1];

        // 开始流式传输 Pod 日志
        podLogStreamer.streamPodLogs(namespace, podName, session);
    }
}

