package com.young.thefastpizzarestfulapi.common.event.handler;

import com.google.common.eventbus.Subscribe;
import com.young.thefastpizzarestfulapi.common.event.StartJobEvent;

import lombok.extern.slf4j.Slf4j;

/**
 * desc:
 *
 * @author Young.
 * @since 2024/5/18 17:32
 */
@Slf4j
public class StartJobEventHandler {

    @Subscribe
    public void handle(StartJobEvent startJobEvent) {
        log.info("startJobEvent: jobId[{}], jobName[{}]", startJobEvent.getJobId(), startJobEvent.getJobName());
    }
}
