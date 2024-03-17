from functools import wraps

from halo import Halo


def lazy_call(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        def inner_call(**late_kwargs):
            complete_kwargs = {**kwargs, **late_kwargs}
            return f(*args, **complete_kwargs)
        return inner_call
    return wrapper


def with_spinner(
        text='Processing...',
        msg_success='Completed!',
        msg_failed='An error occurred!',
        spinner_type='dots'):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            spinner = Halo(text=text, spinner=spinner_type)
            spinner.start()
            try:
                result = func(*args, **kwargs)
                spinner.succeed(msg_success)
                spinner.stop()
                return result
            except Exception as e:
                spinner.fail(msg_failed)
                raise e

        return wrapper

    return decorator
