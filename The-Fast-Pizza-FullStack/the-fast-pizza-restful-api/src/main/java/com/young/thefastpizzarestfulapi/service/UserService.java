package com.young.thefastpizzarestfulapi.service;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.young.thefastpizzarestfulapi.entity.UserDo;
import com.young.thefastpizzarestfulapi.mapper.UserMapper;
import org.springframework.stereotype.Service;



@Service
public class UserService extends ServiceImpl<UserMapper, UserDo> {

    // @Override
    public boolean save(UserDo entity) {
        // System.out.println(bushi);
        return false;
    }

    private void test() {
        save(null);
    }

}
