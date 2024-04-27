package com.fast.young.pizza.fastyoungpizzrestfulapi.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;

import java.time.LocalDate;
import java.util.Date;

@Entity
public class Pizza {


    /*name: "Focaccia",
    ingredients: "Bread with italian olive oil and rosemary",
    price: 6,
    photoName: "pizzas/focaccia.jpg",
    soldOut: false,*/

    @Id
    private Long id;

    private String name;

    private String ingredients;

    @Column(name = "photo_name")
    private String photoName;

    @Column(name = "sold_out")
    private boolean soldOut;

    private Double price;

    @Column(name = "create_date")
    private LocalDate createDate;

    public Pizza() {
    }

    public Pizza(String name, String ingredients, String photoName, boolean soldOut, Double price) {
        this.name = name;
        this.ingredients = ingredients;
        this.photoName = photoName;
        this.soldOut = soldOut;
        this.price = price;
    }


    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getIngredients() {
        return ingredients;
    }

    public void setIngredients(String ingredients) {
        this.ingredients = ingredients;
    }

    public String getPhotoName() {
        return photoName;
    }

    public void setPhotoName(String photoName) {
        this.photoName = photoName;
    }

    public boolean isSoldOut() {
        return soldOut;
    }

    public void setSoldOut(boolean soldOut) {
        this.soldOut = soldOut;
    }

    public Double getPrice() {
        return price;
    }

    public void setPrice(Double price) {
        this.price = price;
    }

    @Override
    public String toString() {
        return "Pizza{" +
                "name='" + name + '\'' +
                ", ingredients='" + ingredients + '\'' +
                ", photoName='" + photoName + '\'' +
                ", soldOut=" + soldOut +
                ", price=" + price +
                '}';
    }
}
