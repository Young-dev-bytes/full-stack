
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pod Logs</title>
</head>
<body>
    <div id="logs"></div>
    <script>
        const namespace = 'default'; // 替换为实际的 namespace
        const podName = 'example-pod'; // 替换为实际的 pod name
        const socket = new WebSocket('ws://localhost:8080/pod-logs');

        socket.onopen = function () {
            socket.send(namespace + ' ' + podName);
        };

        socket.onmessage = function (event) {
            const logsDiv = document.getElementById('logs');
            logsDiv.innerHTML += '<p>' + event.data + '</p>';
        };
    </script>
</body>
</html>

```


使用 `CoreV1Api` 中的 `readNamespacedPodLog` 方法，并将参数 `follow` 设置为 `true` 来获取实时日志，可以避免使用命令行。以下是如何通过该方法实现获取实时日志，并通过 WebSocket 动态显示在页面上的完整示例。

### 步骤一：设置 Kubernetes Java Client

首先，需要在你的项目中添加 Kubernetes Java Client 依赖。在你的 `pom.xml` 中添加以下依赖：

```xml
<dependency>
    <groupId>io.kubernetes</groupId>
    <artifactId>client-java</artifactId>
    <version>13.0.0</version>
</dependency>
```

### 步骤二：编写 Java 代码获取实时日志

编写一个 Java 类，通过 `readNamespacedPodLog` 获取 Pod 的日志。

```java
import io.kubernetes.client.ApiClient;
import io.kubernetes.client.ApiException;
import io.kubernetes.client.Configuration;
import io.kubernetes.client.apis.CoreV1Api;
import io.kubernetes.client.util.Config;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import okhttp3.WebSocket;
import okhttp3.WebSocketListener;
import okio.ByteString;

import java.io.IOException;
import java.util.concurrent.CountDownLatch;

public class PodLogStreamer {

    private ApiClient client;
    private CoreV1Api api;

    public PodLogStreamer() throws IOException {
        // 初始化 Kubernetes 客户端
        client = Config.defaultClient();
        Configuration.setDefaultApiClient(client);
        api = new CoreV1Api(client);
    }

    public void streamPodLogs(String namespace, String podName, WebSocketSession session) {
        String path = "/api/v1/namespaces/" + namespace + "/pods/" + podName + "/log?follow=true";
        OkHttpClient httpClient = client.getHttpClient();

        Request request = new Request.Builder()
                .url(client.getBasePath() + path)
                .build();

        CountDownLatch latch = new CountDownLatch(1);

        httpClient.newWebSocket(request, new WebSocketListener() {
            @Override
            public void onMessage(WebSocket webSocket, String text) {
                try {
                    session.sendMessage(new TextMessage(text));
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }

            @Override
            public void onClosing(WebSocket webSocket, int code, String reason) {
                webSocket.close(code, reason);
                latch.countDown();
            }

            @Override
            public void onFailure(WebSocket webSocket, Throwable t, Response response) {
                t.printStackTrace();
                latch.countDown();
            }
        });

        try {
            latch.await();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```

### 步骤三：设置 WebSocket 服务器

为了将日志实时传输到网页上，我们需要一个 WebSocket 服务器。在这个示例中，使用 Spring Boot 来搭建 WebSocket 服务器。

首先，添加 Spring Boot WebSocket 依赖：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-websocket</artifactId>
</dependency>
```

编写 WebSocket 配置类：

```java
import org.springframework.context.annotation.Configuration;
import org.springframework.web.socket.config.annotation.EnableWebSocket;
import org.springframework.web.socket.config.annotation.WebSocketConfigurer;
import org.springframework.web.socket.config.annotation.WebSocketHandlerRegistry;

@Configuration
@EnableWebSocket
public class WebSocketConfig implements WebSocketConfigurer {

    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
        registry.addHandler(new PodLogWebSocketHandler(), "/pod-logs");
    }
}
```

编写 WebSocket 处理程序：

```java
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

public class PodLogWebSocketHandler extends TextWebSocketHandler {

    private PodLogStreamer podLogStreamer;

    public PodLogWebSocketHandler() throws IOException {
        podLogStreamer = new PodLogStreamer();
    }

    @Override
    public void handleTextMessage(WebSocketSession session, TextMessage message) throws Exception {
        // 从客户端消息中解析 namespace 和 podName
        String[] payload = message.getPayload().split(" ");
        String namespace = payload[0];
        String podName = payload[1];

        // 开始流式传输 Pod 日志
        new Thread(() -> {
            try {
                podLogStreamer.streamPodLogs(namespace, podName, session);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }).start();
    }
}
```

### 步骤四：前端页面展示

最后，编写一个简单的 HTML 页面，通过 WebSocket 接收并显示日志。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pod Logs</title>
</head>
<body>
    <div id="logs"></div>
    <script>
        const namespace = 'default'; // 替换为实际的 namespace
        const podName = 'example-pod'; // 替换为实际的 pod name
        const socket = new WebSocket('ws://localhost:8080/pod-logs');

        socket.onopen = function () {
            socket.send(namespace + ' ' + podName);
        };

        socket.onmessage = function (event) {
            const logsDiv = document.getElementById('logs');
            logsDiv.innerHTML += '<p>' + event.data + '</p>';
        };
    </script>
</body>
</html>
```

### 总结

以上步骤展示了如何通过 `CoreV1Api` 的 `readNamespacedPodLog` 方法获取 Pod 的实时日志，并使用 Spring Boot WebSocket 将日志动态显示在网页上。你可以根据实际需求进一步扩展这个示例，比如增加日志过滤、错误处理等功能。



好的，这里是使用 `CoreV1Api` 中的 `readNamespacedPodLog` 方法并将参数 `follow` 设置为 `true` 以获取实时日志的实现。该实现包括通过 WebSocket 服务器将日志动态传输到前端页面进行显示。

### 步骤一：设置 Kubernetes Java Client

在你的 `pom.xml` 中添加 Kubernetes Java Client 依赖：

```xml
<dependency>
    <groupId>io.kubernetes</groupId>
    <artifactId>client-java</artifactId>
    <version>13.0.0</version>
</dependency>
```

### 步骤二：编写 Java 代码获取实时日志

编写一个 Java 类，通过 `readNamespacedPodLog` 获取 Pod 的实时日志。

```java
import io.kubernetes.client.ApiClient;
import io.kubernetes.client.ApiException;
import io.kubernetes.client.Configuration;
import io.kubernetes.client.apis.CoreV1Api;
import io.kubernetes.client.util.Config;
import okhttp3.Response;
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
        try (Response response = api.readNamespacedPodLogCall(podName, namespace, null, null, null, null, null, null, null, true, null).execute()) {
            BufferedReader reader = new BufferedReader(new InputStreamReader(response.body().byteStream()));

            String line;
            while ((line = reader.readLine()) != null) {
                session.sendMessage(new TextMessage(line));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### 步骤三：设置 WebSocket 服务器

为了将日志实时传输到网页上，我们需要一个 WebSocket 服务器。在这个示例中，使用 Spring Boot 来搭建 WebSocket 服务器。

首先，添加 Spring Boot WebSocket 依赖：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-websocket</artifactId>
</dependency>
```

编写 WebSocket 配置类：

```java
import org.springframework.context.annotation.Configuration;
import org.springframework.web.socket.config.annotation.EnableWebSocket;
import org.springframework.web.socket.config.annotation.WebSocketConfigurer;
import org.springframework.web.socket.config.annotation.WebSocketHandlerRegistry;

@Configuration
@EnableWebSocket
public class WebSocketConfig implements WebSocketConfigurer {

    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
        registry.addHandler(new PodLogWebSocketHandler(), "/pod-logs");
    }
}
```

编写 WebSocket 处理程序：

```java
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

public class PodLogWebSocketHandler extends TextWebSocketHandler {

    private PodLogStreamer podLogStreamer;

    public PodLogWebSocketHandler() throws Exception {
        podLogStreamer = new PodLogStreamer();
    }

    @Override
    public void handleTextMessage(WebSocketSession session, TextMessage message) {
        String[] payload = message.getPayload().split(" ");
        String namespace = payload[0];
        String podName = payload[1];

        new Thread(() -> {
            try {
                podLogStreamer.streamPodLogs(namespace, podName, session);
            } catch (ApiException e) {
                e.printStackTrace();
            }
        }).start();
    }
}
```

### 步骤四：前端页面展示

编写一个简单的 HTML 页面，通过 WebSocket 接收并显示日志。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pod Logs</title>
</head>
<body>
    <div id="logs"></div>
    <script>
        const namespace = 'default'; // 替换为实际的 namespace
        const podName = 'example-pod'; // 替换为实际的 pod name
        const socket = new WebSocket('ws://localhost:8080/pod-logs');

        socket.onopen = function () {
            socket.send(namespace + ' ' + podName);
        };

        socket.onmessage = function (event) {
            const logsDiv = document.getElementById('logs');
            logsDiv.innerHTML += '<p>' + event.data + '</p>';
        };
    </script>
</body>
</html>
```

### 总结

以上步骤展示了如何通过 `CoreV1Api` 的 `readNamespacedPodLog` 方法获取 Pod 的实时日志，并使用 Spring Boot WebSocket 将日志动态显示在网页上。通过这种方式，可以实时监控 Kubernetes Pod 的日志，并在前端页面上动态展示。

