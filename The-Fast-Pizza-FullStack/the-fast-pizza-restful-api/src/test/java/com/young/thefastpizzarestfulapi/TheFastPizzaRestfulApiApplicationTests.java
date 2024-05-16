package com.young.thefastpizzarestfulapi;

import com.young.thefastpizzarestfulapi.entity.PizzaDo;
import com.young.thefastpizzarestfulapi.mapper.PizzaMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;


@SpringBootTest
class TheFastPizzaRestfulApiApplicationTests {

    @Autowired
    private PizzaMapper pizzaMapper;


    void contextLoads() {
        PizzaDo pizzaDo = pizzaMapper.selectById(1001);
        System.out.println(pizzaDo);
    }



}
