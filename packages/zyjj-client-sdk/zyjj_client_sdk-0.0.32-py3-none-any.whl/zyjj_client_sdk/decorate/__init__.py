# 积分使用装饰器，调用函数前会检查积分，执行完毕后会自动扣除积分
# desc可以使用 “{input[key]}”
def point_use(point: int, name: str, desc=''):
    def decorator(func):
        def wrapper(*args, **kwargs):
            api = args[0]
            data = args[1]
            # 函数执行前检查用户积分
            api.point_check(point)
            # 执行函数获取结果
            result = func(*args, **kwargs)
            # 执行后扣除对应积分
            api.point_use(name, point, desc.format(input=data, output=result))
            return result

        return wrapper

    return decorator
