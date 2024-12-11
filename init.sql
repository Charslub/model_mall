
-- ----------------------------
-- 用户表
-- ----------------------------
CREATE TABLE IF NOT EXISTS users(
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(256) NOT NULL DEFAULT '' COMMENT '用户名',
    password VARCHAR(128) NOT NULL COMMENT '密码',
    avatar VARCHAR(256) NOT NULL DEFAULT '' COMMENT '用户头像',
    role ENUM('user', 'admin', 'merchant', 'super') NOT NULL DEFAULT 'user' COMMENT '用户角色',
    is_disable TINYINT DEFAULT 0 COMMENT '是否禁用',
    delete_flag TINYINT DEFAULT 0,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT '用户表';

-- ----------------------------
-- 模型表
-- ----------------------------
CREATE TABLE IF NOT EXISTS models(
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uid BIGINT UNSIGNED NOT NULL COMMENT '用户id',
    model_name VARCHAR(256) NOT NULL DEFAULT '' COMMENT '模型名称',
    img_url VARCHAR(512) NOT NULL DEFAULT '' COMMENT '模型图片链接',
    is_available TINYINT DEFAULT 1 COMMENT '是否上架',
    delete_flag TINYINT DEFAULT 0,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_uid` (`uid`)
) COMMENT '模型表';

-- ----------------------------
-- 模型类型表
-- ----------------------------
CREATE TABLE IF NOT EXISTS types(
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    type_name VARCHAR(256) NOT NULL DEFAULT '' COMMENT '用户名',
    type_level INT DEFAULT 0 COMMENT '类型等级',
    is_system TINYINT DEFAULT 1 COMMENT '是否为系统类型',
    delete_flag TINYINT DEFAULT 0,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT '模型类型表';

-- ----------------------------
-- 模型类型对应表
-- ----------------------------
CREATE TABLE IF NOT EXISTS models_types(
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    model_id BIGINT UNSIGNED NOT NULL COMMENT '模型id',
    type_id BIGINT UNSIGNED NOT NULL COMMENT '类型id',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT '模型类型关系表';
