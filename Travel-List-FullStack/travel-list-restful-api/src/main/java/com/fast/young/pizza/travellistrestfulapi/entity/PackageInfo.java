package com.fast.young.pizza.travellistrestfulapi.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;

import java.time.LocalDate;

@Entity(name = "package_info")
public class PackageInfo {


    // const initialItems = [
    //   { id: 1, description: "Passports", quantity: 2, packed: false },
    //   { id: 2, description: "Socks", quantity: 12, packed: true },
    // ];

    @Id
    private Long id;

    private String description;

    private Integer quantity;

    private boolean packed;

    @Column(name = "create_date")
    private LocalDate createDate;

    public PackageInfo() {
    }

    public PackageInfo(Long id, String description, Integer quantity, boolean packed) {
        this.id = id;
        this.description = description;
        this.quantity = quantity;
        this.packed = packed;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Integer getQuantity() {
        return quantity;
    }

    public void setQuantity(Integer quantity) {
        this.quantity = quantity;
    }

    public boolean isPacked() {
        return packed;
    }

    public void setPacked(boolean packed) {
        this.packed = packed;
    }

    @Override
    public String toString() {
        return "PackageInfo{" +
                "id=" + id +
                ", description='" + description + '\'' +
                ", quantity=" + quantity +
                ", packed=" + packed +
                '}';
    }
}
