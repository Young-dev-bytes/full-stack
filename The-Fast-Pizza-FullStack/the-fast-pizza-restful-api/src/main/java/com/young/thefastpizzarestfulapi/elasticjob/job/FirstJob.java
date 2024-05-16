package com.young.thefastpizzarestfulapi.elasticjob.job;

import org.apache.shardingsphere.elasticjob.api.ShardingContext;
import org.apache.shardingsphere.elasticjob.simple.job.SimpleJob;
import org.springframework.stereotype.Component;

@Component
public class FirstJob implements SimpleJob {
    @Override
    public void execute(ShardingContext shardingContext) {

        // System.out.println("first job");

        /*int shardingItem = shardingContext.getShardingItem();

        System.out.println(shardingContext.getShardingParameter());
        System.out.println(shardingItem);
        if (shardingItem == 0) {

            System.out.println("first job");

        }*/
    }
}
