package com.young.thefastpizzarestfulapi;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@MapperScan("com.young.thefastpizzarestfulapi.mapper")
public class TheFastPizzaRestfulApiApplication {

    public static void main(String[] args) {
        SpringApplication.run(TheFastPizzaRestfulApiApplication.class, args);
    }

}
