
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
    price DECIMAL(10, 2) NOT NULL COMMENT '用户id',
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

-- ----------------------------
-- 订单表
-- ----------------------------
CREATE TABLE IF NOT EXISTS orders(
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uid BIGINT UNSIGNED NOT NULL COMMENT '用户id',
    total_price DECIMAL(10, 2) NOT NULL COMMENT '订单总金额',
    status ENUM('pending', 'paid', 'shipped') NOT NULL DEFAULT 'pending' COMMENT '订单状态',
    delete_flag TINYINT DEFAULT 0 COMMENT '是否删除',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT '订单表';

-- ----------------------------
-- 订单模型表
-- ----------------------------
CREATE TABLE IF NOT EXISTS order_models(
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    order_id BIGINT UNSIGNED NOT NULL COMMENT '订单id',
    model_id BIGINT UNSIGNED NOT NULL COMMENT '模型id',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT '订单模型关系表';

-- ----------------------------
-- 用户钱包表
-- ----------------------------
CREATE TABLE IF NOT EXISTS user_wallet(
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uid BIGINT UNSIGNED NOT NULL COMMENT '用户id',
    balance DECIMAL(10, 2) NOT NULL DEFAULT 0.0 COMMENT '钱包余额',
    delete_flag TINYINT NOT NULL DEFAULT 0 COMMENT '是否作废',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT '用户钱包表';

