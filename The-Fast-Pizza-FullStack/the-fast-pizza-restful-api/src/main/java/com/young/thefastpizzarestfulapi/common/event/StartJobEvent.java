package com.young.thefastpizzarestfulapi.common.event;

import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * desc:
 *
 * @author Young.
 * @since 2024/5/18 17:35
 */
@Data
@AllArgsConstructor
public class StartJobEvent {

    private String jobId;

    private String jobName;
}
