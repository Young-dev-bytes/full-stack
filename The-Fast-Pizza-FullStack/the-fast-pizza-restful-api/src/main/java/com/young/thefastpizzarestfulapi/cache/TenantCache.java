package com.young.thefastpizzarestfulapi.cache;

import org.springframework.stereotype.Component;

import java.util.concurrent.ExecutionException;

@Component
public class TenantCache extends GuavaCache<String, String> {

    public TenantCache() {
        super();
    }

    @Override
    protected String fetchData(String key) {
        System.out.println("key:" + key);
        System.out.println("start fetching data...");
        return "tenantCode";
    }

    public static void main(String[] args) throws ExecutionException {
        String tenantCode = new TenantCache().getValue("tenantCode");
        System.out.println("tenantCode:" + tenantCode);
    }
}
