package com.young.thefastpizzarestfulapi.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.young.thefastpizzarestfulapi.entity.PizzaDo;
import com.young.thefastpizzarestfulapi.entity.UserDo;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface PizzaMapper extends BaseMapper<PizzaDo> {

}

