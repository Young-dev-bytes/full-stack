package com.young.thefastpizzarestfulapi.entity;

import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

@Data
@TableName("user")
public class UserDo {

    private Long id;

    private String name;

    private Integer age;

    private String email;
}
