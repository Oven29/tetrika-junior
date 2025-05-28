import inspect


def strict(func):
    """
        Декоратор, проверяющий типы аргументов,
        выбрасывает TypeError в случае несоответствия
    """
    sig = inspect.signature(func)
    annotations = func.__annotations__

    def wrapper(*args, **kwargs):
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        for name, value in bound_args.arguments.items():
            expected_type = annotations.get(name)
            if expected_type and not isinstance(value, expected_type):
                raise TypeError(
                    f"Argument '{name}' must be of type {expected_type.__name__}, "
                    f"got {type(value).__name__}"
                )
        return func(*args, **kwargs)

    return wrapper



@strict
def sum_two(a: int, b: int) -> int:
    return a + b


print(sum_two(1, 2))    # >>> 3
print(sum_two(1, 2.4))  # >>> TypeError
