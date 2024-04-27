package com.young.thefastpizzarestfulapi;

import com.young.thefastpizzarestfulapi.entity.PizzaDo;
import com.young.thefastpizzarestfulapi.entity.UserDo;
import com.young.thefastpizzarestfulapi.mapper.PizzaMapper;
import com.young.thefastpizzarestfulapi.mapper.UserMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;


@SpringBootTest
class TheFastPizzaRestfulApiApplicationTests {

    // @Autowired
    // private UserMapper userMapper;

    @Autowired
    private PizzaMapper pizzaMapper;


    @Test
    void contextLoads() {
        // UserDo user = userMapper.selectById(1);
        // System.out.println(user);
        PizzaDo pizzaDo = pizzaMapper.selectById(1001);
        System.out.println(pizzaDo);
    }



}
