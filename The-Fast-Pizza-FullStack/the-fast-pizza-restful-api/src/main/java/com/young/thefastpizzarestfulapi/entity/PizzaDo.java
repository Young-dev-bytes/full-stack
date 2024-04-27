package com.young.thefastpizzarestfulapi.entity;


import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.time.LocalDate;

@Data
@TableName("pizza")
public class PizzaDo {

    private Long id;

    private String name;

    private String ingredients;

    private String photoName;

    private boolean soldOut;

    private Double price;

    private LocalDate createDate;

}

