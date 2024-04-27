package com.young.thefastpizzarestfulapi.entity;


import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.time.LocalDate;

@Data
@TableName("t_pizza")
public class PizzaDo {

    private Long id;

    private String name;

    private String ingredients;

    private String unitPrice;

    private String imageUrl;

    private String soldOut;

    private LocalDate createTime;
}

