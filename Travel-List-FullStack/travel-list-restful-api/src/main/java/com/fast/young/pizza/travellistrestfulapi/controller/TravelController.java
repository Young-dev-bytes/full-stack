package com.fast.young.pizza.travellistrestfulapi.controller;


import com.fast.young.pizza.travellistrestfulapi.entity.PackageInfo;
import com.fast.young.pizza.travellistrestfulapi.jpa.TravelListRepository;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class TravelController {

    private final TravelListRepository travelListRepository;


    public TravelController(TravelListRepository travelListRepository) {
        this.travelListRepository = travelListRepository;
    }

    @GetMapping("/retrieveTravelList")
    public List<PackageInfo> retrieveTravelList() throws InterruptedException {
        Thread.sleep(2000);
        return travelListRepository.findAll();
    }

}
