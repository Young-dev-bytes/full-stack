package com.young.thefastpizzarestfulapi.event;

import com.young.thefastpizzarestfulapi.common.event.ErrorJobEvent;
import com.young.thefastpizzarestfulapi.common.event.JobEventRegisterCenter;
import com.young.thefastpizzarestfulapi.common.event.StartJobEvent;
import org.junit.jupiter.api.Test;

/**
 * desc:
 *
 * @author Young.
 * @since 2024/5/18 17:39
 */
public class Test_EventBus {

    @Test
    void test_eventBus() {
        JobEventRegisterCenter.post(new StartJobEvent("jobId","jobName"));
        JobEventRegisterCenter.post(new ErrorJobEvent("38298","job-error"));
    }
}
