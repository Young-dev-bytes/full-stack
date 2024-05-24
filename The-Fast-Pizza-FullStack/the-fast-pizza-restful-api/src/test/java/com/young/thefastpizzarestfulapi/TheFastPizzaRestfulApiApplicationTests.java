package com.young.thefastpizzarestfulapi;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import com.young.thefastpizzarestfulapi.entity.PizzaDo;
import com.young.thefastpizzarestfulapi.mapper.PizzaMapper;

@SpringBootTest
class TheFastPizzaRestfulApiApplicationTests {

    @Autowired
    private PizzaMapper pizzaMapper;

    void contextLoads() {
        PizzaDo pizzaDo = pizzaMapper.selectById(1001);
        System.out.println(pizzaDo);
    }

}
