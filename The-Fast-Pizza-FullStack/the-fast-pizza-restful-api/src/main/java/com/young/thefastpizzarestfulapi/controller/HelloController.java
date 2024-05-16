package com.young.thefastpizzarestfulapi.controller;

import com.young.thefastpizzarestfulapi.cache.TenantCache;
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


}
















