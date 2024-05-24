package com.young.thefastpizzarestfulapi.controller;

import com.young.thefastpizzarestfulapi.common.cache.TenantCache;
import io.kubernetes.client.openapi.apis.CoreV1Api;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.concurrent.ExecutionException;

@RestController
public class HelloController {

    @Autowired
    private TenantCache tenantCache;

    @GetMapping("/hello")
    public String hello() throws ExecutionException {
        return tenantCache.getValue("tenantCode");
    }


    public static void main(String[] args) {

        CoreV1Api coreV1Api = new CoreV1Api(null);

        // coreV1Api.readNamespacedPodLog("")
    }


}
















