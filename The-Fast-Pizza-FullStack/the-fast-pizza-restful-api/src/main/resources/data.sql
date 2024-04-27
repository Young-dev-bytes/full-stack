DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`
(
    id    BIGINT NOT NULL COMMENT '主键ID',
    name  VARCHAR(30) NULL DEFAULT NULL COMMENT '姓名',
    age   INT NULL DEFAULT NULL COMMENT '年龄',
    email VARCHAR(50) NULL DEFAULT NULL COMMENT '邮箱',
    PRIMARY KEY (id)
);
INSERT INTO `user` (id, name, age, email)
VALUES (1, 'Jone', 18, 'test1@baomidou.com'),
       (2, 'Jack', 20, 'test2@baomidou.com'),
       (3, 'Tom', 28, 'test3@baomidou.com'),
       (4, 'Sandy', 21, 'test4@baomidou.com'),
       (5, 'Billie', 24, 'test5@baomidou.com');



DROP TABLE IF EXISTS `t_pizza`;
CREATE TABLE `t_pizza`
(
    id          BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT 'primary id',
    name        VARCHAR(30) DEFAULT NULL COMMENT 'pizza name',
    unit_price  VARCHAR(30) DEFAULT NULL COMMENT 'pizza price',
    image_url   VARCHAR(30) DEFAULT NULL COMMENT 'pizza image url',
    ingredients VARCHAR(30) DEFAULT NULL COMMENT 'pizza ingredients',
    sold_out    CHAR(1)     DEFAULT '0' COMMENT 'status（0 true 1 false）',
    create_by   VARCHAR(64) DEFAULT '' COMMENT 'create user',
    create_time DATETIME COMMENT 'create time',
    update_by   VARCHAR(64) DEFAULT '' COMMENT 'update user',
    update_time DATETIME COMMENT 'update time',
    PRIMARY KEY (id)
)ENGINE=INNODB AUTO_INCREMENT=1001 COMMENT = 'pizza info table';


/*
insert into t_pizza (id, name, ingredients, unit_price, image_url, sold_out, create_time)
values (10001, 'Focaccia', 'Bread with italian olive oil and rosemary', 6, 'pizzas/focaccia.jpg', false,
        CURRENT_DATE());


insert into t_pizza (id, name, ingredients, unit_price, image_url, sold_out, create_time)
values (10002, 'Pizza Margherita', 'Tomato and mozarella', 10, 'pizzas/margherita.jpg', false,
        CURRENT_DATE());


insert into t_pizza (id, name, ingredients, unit_price, image_url, sold_out, create_time)
values (10003, 'Pizza Spinaci', 'Tomato, mozarella, spinach, and ricotta cheese', 12, 'pizzas/spinaci.jpg', false,
        CURRENT_DATE());


insert into t_pizza (id, name, ingredients, unit_price, image_url, sold_out, create_time)
values (10004, 'Pizza Salamino', 'Tomato, mozarella, and pepperoni', 15, 'pizzas/salamino.jpg', true,
        CURRENT_DATE());

insert into t_pizza (id, name, ingredients, unit_price, image_url, sold_out, create_time)
values (10005, 'Pizza Prosciutto"', 'Tomato, mozarella, ham, aragula, and burrata cheese', 18, 'pizzas/prosciutto.jpg', false,
        CURRENT_DATE());

insert into t_pizza (id, name, ingredients, unit_price, image_url, sold_out, create_time)
values (10006, 'Pizza Funghi"', 'Tomato, mozarella, mushrooms, and onion', 12, 'pizzas/funghi.jpg', false,
        CURRENT_DATE());*/



