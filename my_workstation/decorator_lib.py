def do_twice(func):
    def wrapper_do_twice():
        func()
        func()
    return wrapper_do_twice
