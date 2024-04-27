package com.fast.young.pizza.travellistrestfulapi.jpa;

import com.fast.young.pizza.travellistrestfulapi.entity.PackageInfo;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TravelListRepository extends JpaRepository<PackageInfo, Long> {


}
