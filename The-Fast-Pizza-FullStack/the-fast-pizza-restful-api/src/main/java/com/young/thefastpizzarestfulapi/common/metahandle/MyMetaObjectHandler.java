package com.young.thefastpizzarestfulapi.common.metahandle;

import com.baomidou.mybatisplus.core.handlers.MetaObjectHandler;
import com.young.thefastpizzarestfulapi.entity.basic.BusinessEntity;
import org.apache.ibatis.reflection.MetaObject;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * desc:
 *
 * @author Young.
 */
@Component
public class MyMetaObjectHandler implements MetaObjectHandler {

    @Override
    public void insertFill(MetaObject metaObject) {
        LocalDateTime now = LocalDateTime.now();
        fillStrategy(metaObject, "createTime", now);
        fillStrategy(metaObject, "updateTime", now);

        String account = "cw0106718";
        setFieldValByName("createUser", account, metaObject);
        setFieldValByName("updateUser", account, metaObject);

        // businessEntity handle tenant and project
        if (metaObject.getOriginalObject() instanceof BusinessEntity) {
            setFieldValByName("projectId", "890", metaObject);
        }

    }

    @Override
    public void updateFill(MetaObject metaObject) {
        String account = "0106718";
        setFieldValByName("updateUser", account, metaObject);
        setFieldValByName("updateTime", LocalDateTime.now(), metaObject);
    }
}
