package com.fast.young.pizza.fastyoungpizzrestfulapi.jpa;

import com.fast.young.pizza.fastyoungpizzrestfulapi.entity.Pizza;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PizzasRepository extends JpaRepository<Pizza, Long> {


}
