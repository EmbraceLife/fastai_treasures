
# count the number of runs
import functools

def count_calls(func):
    #    @functools.wraps(func)
    def wrapper_count_calls(*args, **kwargs):
        wrapper_count_calls.num_calls += 1
        print(f"Call {wrapper_count_calls.num_calls} of {func.__name__!r}")
        return func(*args, **kwargs)
    wrapper_count_calls.num_calls = 0 # recount again when @count_calls again
    return wrapper_count_calls

@count_calls
def say_whee():
    print("Whee!")

say_whee()
say_whee()
say_whee()


# count the number of runs
import functools

def count_calls(func):
    @functools.wraps(func)
    def wrapper_count_calls(*args, **kwargs):
        wrapper_count_calls.num_calls += 1
        print(f"Call {wrapper_count_calls.num_calls} of {func.__name__!r}")
        return func(*args, **kwargs)
    wrapper_count_calls.num_calls = 0 # recount again when @count_calls again
    return wrapper_count_calls

@count_calls
def say_whee():
    print("Whee!")

say_whee()
say_whee()
say_whee()

# count the number of runs
import functools

def count_calls(func):
    def wrapper_count_calls(*args, **kwargs):
        wrapper_count_calls.num_calls += 1
        print(f"Call {wrapper_count_calls.num_calls} of {func.__name__!r}")
        return func(*args, **kwargs)
    wrapper_count_calls.num_calls = 0 # recount again when @count_calls again
    @functools.wraps(func)
    return wrapper_count_calls

@count_calls
def say_whee():
    print("Whee!")

say_whee()
say_whee()
say_whee()

