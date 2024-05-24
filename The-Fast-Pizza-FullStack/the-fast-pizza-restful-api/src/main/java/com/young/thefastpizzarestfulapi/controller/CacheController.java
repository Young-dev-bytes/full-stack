package com.young.thefastpizzarestfulapi.controller;

import com.young.thefastpizzarestfulapi.common.cache.TenantCache;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.concurrent.ExecutionException;

/**
 * desc:
 *
 * @author Young.
 * @since 2024/5/18 18:20
 */

@RestController
public class CacheController {

    private final TenantCache tenantCache;

    public CacheController(TenantCache tenantCache) {
        this.tenantCache = tenantCache;
    }

    @GetMapping("/cache")
    public String cache() throws ExecutionException {
        return tenantCache.getValue("tenantCode");
    }

}
