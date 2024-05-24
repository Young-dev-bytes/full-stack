package com.young.thefastpizzarestfulapi.common.event;

import com.google.common.eventbus.AsyncEventBus;
import com.young.thefastpizzarestfulapi.common.event.handler.ErrorJobEventHandler;
import com.young.thefastpizzarestfulapi.common.event.handler.StartJobEventHandler;
import com.young.thefastpizzarestfulapi.utils.ThreadPoolUtils;

/***
 * event register center
 * 
 * @author share
 */

public class JobEventRegisterCenter {

    private static final AsyncEventBus EVENT_BUS = new AsyncEventBus(ThreadPoolUtils.getThreadPoolExecutor());

    static {
        EVENT_BUS.register(new StartJobEventHandler());
        EVENT_BUS.register(new ErrorJobEventHandler());
    }

    public JobEventRegisterCenter() {}

    public static void post(Object event) {
        EVENT_BUS.post(event);
    }
}
