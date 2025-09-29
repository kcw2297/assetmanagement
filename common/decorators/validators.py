import inspect
from collections.abc import Callable
from functools import wraps


def validate_range(param_name: str, min_value: float | None = None, max_value: float | None = None):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            sig = inspect.signature(func)
            params = list(sig.parameters.keys())

            if param_name in kwargs:
                value = kwargs[param_name]
            else:
                try:
                    param_index = params.index(param_name)
                    if param_index < len(args):
                        value = args[param_index]
                    else:
                        value = sig.parameters[param_name].default
                except (ValueError, IndexError):
                    return func(*args, **kwargs)

            if value is not None:
                if not isinstance(value, (int, float)):
                    raise TypeError(f"{param_name}은(는) 숫자여야 합니다. 현재 타입: {type(value).__name__}")

                if min_value is not None and value < min_value:
                    raise ValueError(f"{param_name}은(는) {min_value} 이상이어야 합니다. 현재 값: {value}")

                if max_value is not None and value > max_value:
                    raise ValueError(f"{param_name}은(는) {max_value} 이하여야 합니다. 현재 값: {value}")

            return func(*args, **kwargs)

        return wrapper
    return decorator