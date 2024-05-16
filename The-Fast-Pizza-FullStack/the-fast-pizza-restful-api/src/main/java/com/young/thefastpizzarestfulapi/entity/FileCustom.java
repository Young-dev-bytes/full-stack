package com.young.thefastpizzarestfulapi.entity;


import lombok.Data;

@Data
public class FileCustom {

    private String id;

    private String name;

    private String type;

    private String content;

    private Boolean backedUp = false;

    public FileCustom(String id, String name, String type, String content) {
        this.id = id;
        this.name = name;
        this.type = type;
        this.content = content;
    }
}
