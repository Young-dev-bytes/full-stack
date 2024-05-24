package com.young.thefastpizzarestfulapi.common.event;

import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * desc:
 *
 * @author Young.
 * @since 2024/5/18 17:59
 */
@Data
@AllArgsConstructor
public class ErrorJobEvent {

    private String jobId;

    private String jobName;

}
