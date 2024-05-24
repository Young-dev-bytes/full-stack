package com.young.thefastpizzarestfulapi.common.event.handler;

import com.google.common.eventbus.Subscribe;
import com.young.thefastpizzarestfulapi.common.event.ErrorJobEvent;

import lombok.extern.slf4j.Slf4j;

/**
 * desc:
 *
 * @author Young.
 * @since 2024/5/18 17:58
 */
@Slf4j
public class ErrorJobEventHandler {

    @Subscribe
    public void handle(ErrorJobEvent errorJobEvent) {
        log.info("errorJobEvent: jobId[{}], jobName[{}]", errorJobEvent.getJobId(), errorJobEvent.getJobName());

    }
}
