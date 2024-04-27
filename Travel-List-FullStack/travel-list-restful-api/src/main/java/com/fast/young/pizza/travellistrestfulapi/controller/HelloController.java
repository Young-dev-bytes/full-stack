package com.fast.young.pizza.travellistrestfulapi.controller;


import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {


    @GetMapping("hello")
    public String hello() {
        return "hello";
    }
}
