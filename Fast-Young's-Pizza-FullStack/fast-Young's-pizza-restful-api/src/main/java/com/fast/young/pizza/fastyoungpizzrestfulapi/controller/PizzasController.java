package com.fast.young.pizza.fastyoungpizzrestfulapi.controller;


import com.fast.young.pizza.fastyoungpizzrestfulapi.entity.Pizza;
import com.fast.young.pizza.fastyoungpizzrestfulapi.jpa.PizzasRepository;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class PizzasController {

    private final PizzasRepository pizzasRepository;

    public PizzasController(PizzasRepository pizzasRepository) {
        this.pizzasRepository = pizzasRepository;
    }

    @GetMapping("/retrievePizzas")
    public List<Pizza> retrievePizzas() throws InterruptedException {
        // List<Pizza> pizzas = new ArrayList<>();
        Thread.sleep(4000);
        return pizzasRepository.findAll();
    }
}
