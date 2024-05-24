package com.young.thefastpizzarestfulapi.utils;

import java.util.concurrent.Executor;
import java.util.concurrent.Executors;

/**
 * desc:
 *
 * @author Young.
 * @since 2024/5/18 17:35
 */
public class ThreadPoolUtils {

    public static Executor getThreadPoolExecutor() {
        return Executors.newSingleThreadExecutor();
    }
}
