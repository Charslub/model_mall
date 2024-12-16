from django.core.cache import cache


# 设置缓存值
def set_value(key, value, timeout=None):
    """
    设置缓存值
    :param key: Redis 键
    :param value: Redis 值
    :param timeout: 可选的过期时间，单位为秒
    :return: 是否成功
    """
    try:
        if timeout:
            cache.set(key, value, timeout)  # 设置值并设置过期时间
        else:
            cache.set(key, value)  # 设置值，不设置过期时间
        return True
    except Exception as e:
        print(f"Error setting value: {e}")
        return False


# 获取缓存值
def get_value(key):
    """
    获取缓存值
    :param key: Redis 键
    :return: Redis 值，如果键不存在则返回 None
    """
    try:
        value = cache.get(key)
        return value
    except Exception as e:
        print(f"Error getting value: {e}")
        return None


# 删除缓存值
def delete_value(key):
    """
    删除缓存值
    :param key: Redis 键
    :return: 是否删除成功
    """
    try:
        cache.delete(key)
        return True
    except Exception as e:
        print(f"Error deleting value: {e}")
        return False


# 更新缓存值
def update_value(key, value, timeout=None):
    """
    更新缓存值
    :param key: Redis 键
    :param value: 新的 Redis 值
    :param timeout: 可选的过期时间，单位为秒
    :return: 是否更新成功
    """
    try:
        if cache.get(key):  # 检查键是否存在
            set_value(key, value, timeout)
            return True
        else:
            print(f"Key '{key}' does not exist")
            return False
    except Exception as e:
        print(f"Error updating value: {e}")
        return False
