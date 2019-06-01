# ## Decorators
# %%
def add_one(number):
    return number + 1

add_one(2)
# %%
def say_hello(name):
    return f"Hello {name}"

def be_awesome(name):
    return f"Yo {name}, together we are the awesomest!"

def greet_bob(greeter_func):
    return greeter_func("Bob")
# %%
greet_bob(say_hello)
greet_bob(be_awesome)
# %%
def parent():
    print("Printing from the parent() function")

    def first_child():
        print("Printing from the first_child() function")

    def second_child():
        print("Printing from the second_child() function")

    second_child()
    first_child()
# %%
parent()
# %%
# parent.first_child()
# %%
def parent(num):
    def first_child():
        return "Hi, I am Emma"

    def second_child():
        return "Call me Liam"

    if num == 1:
        return first_child
    else:
        return second_child
# %%
parent(1)(), parent(0)(), parent(5)
# %%
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

def say_whee():
    print("Whee!")

# this is decoration below
say_whee = my_decorator(say_whee)
# %%
say_whee()
# %% markdown
# ### Syntatic Sugar on decorator
# %%
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

# @my_decorator is just an easier way of saying
# say_whee = my_decorator(say_whee).
@my_decorator
def say_whee():
    print("Whee!")
# %%
say_whee()
# %% markdown
# #### Reusing decorator
# %%
# %%writefile decorator_lib.py
def do_twice(func):
    def wrapper_do_twice():
        func()
        func()
    return wrapper_do_twice
# %%
from decorator_lib import do_twice
@do_twice
def say_whee():
    print("Whee!")

say_whee()
# %% markdown
# #### args and kwargs
# %%
# from decorator_lib import do_twice

@do_twice
def greet(name):
    print(f"Hello {name}")

# greet("kenny")
# %%
def do_twice(func):
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        func(*args, **kwargs)
    return wrapper_do_twice
# %%
@do_twice
def greet(name):
    print(f"Hello {name}")

@do_twice
def shout():
    print("this is me")

greet("kenny"), shout()
# %% markdown
# #### return value
# %%
def do_twice(func):
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        func(*args, **kwargs)
    return wrapper_do_twice
# %%
@do_twice
def return_greeting(name):
    print("Creating greeting")
    return f"Hi {name}" # this line won't executed in previous `wrapper_do_twice'

return_greeting("kenny") # but return values are eaten
# %%
def do_twice(func):
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper_do_twice
# %%
@do_twice
def return_greeting(name):
    print("Creating greeting")
    return f"Hi {name}" # this line will be executed in the return line of
                        # wrapper_to_twice above

return_greeting("kenny") # but return values are eaten
# %% markdown
# #### Who are you, really?
# %%
def do_twice(func):
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper_do_twice
# %%
@do_twice
def return_greeting(name):
    print("Creating greeting")
    return f"Hi {name}"

return_greeting("kenny") # but return values are eaten
# %%
return_greeting # this function is fully buried by wrapper
# %%
return_greeting.__name__ # so the name is messed up
# %%
import functools

def do_twice(func):
    @functools.wraps(func) # fix the name problem
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        return func(*args, **kwargs) # to
    return wrapper_do_twice
# %%
@do_twice
def return_greeting(name):
    print("Creating greeting")
    return f"Hi {name}"

return_greeting("kenny")
# %%
return_greeting.__name__ # its original name is returned
# %% markdown
# The @functools.wraps decorator uses the function `functools.update_wrapper()`
# to update special attributes like __name__ and __doc__
# that are used in the introspection.
# %% markdown
# ### Real world example
# %% markdown
# #### basic template
# %%
import functools

def decorator(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        # Do something before
        value = func(*args, **kwargs)
        # Do something after
        return value
    return wrapper_decorator
# %%
import functools
import time

def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()    # 1
        value = func(*args, **kwargs) # just to waste time
        print(value)
        end_time = time.perf_counter()      # 2
        run_time = end_time - start_time    # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
#         return value
    return wrapper_timer

@timer
def waste_some_time(num_times):
    for _ in range(num_times):
        sum([i**2 for i in range(10000)])
# %%
waste_some_time(2)
# %% markdown
# #### Decorator for Debugger
# %%
import functools

def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]                      # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)           # 3
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")           # 4
        return value
    return wrapper_debug
# %%
@debug
def make_greeting(name, age=None):
    if age is None:
        return f"Howdy {name}!"
    else:
        return f"Whoa {name}! {age} already, you are growing up!"
# %%
make_greeting("Benjamin")
# %%
make_greeting(name="Dorrisile", age=116)
# %% markdown
# #### math func you don't call directly
# %%
import math

# directly doing a decorator to a standard library function
math.factorial = debug(math.factorial)

# use it inside another function, so indirectly
def approximate_e(terms=18):
    return sum(1 / math.factorial(n) for n in range(terms))
# %%
math.factorial(4)
# %%
approximate_e(5)
# %% markdown
# #### slow down code
# %%
import functools
import time

def slow_down(func):
    """Sleep 1 second before calling the function"""
    @functools.wraps(func)
    def wrapper_slow_down(*args, **kwargs):
        time.sleep(1)
        return func(*args, **kwargs)
    return wrapper_slow_down

@slow_down
def countdown(from_number):
    if from_number < 1:
        print("Liftoff!")
    else:
        print(from_number)
        countdown(from_number - 1) # recursive as a decorator
# %%
countdown(5)
# %% markdown
# #### Registering plugin
# %%
import random
PLUGINS = dict()

def register(func):
    """Register a function as a plug-in"""
    PLUGINS[func.__name__] = func
    return func

@register
def say_hello(name):
    return f"Hello {name}"

@register
def be_awesome(name):
    return f"Yo {name}, together we are the awesomest!"

def randomly_greet(name):
    greeter, greeter_func = random.choice(list(PLUGINS.items()))
    # random.choice
    print(f"Using {greeter!r}")
    return greeter_func(name)
# %%
PLUGINS
# %%
say_hello('kenny')
# %%
randomly_greet('daniel')
# %% markdown
# The main benefit of this simple plugin architecture is that you do not need
 # to maintain a list of which plugins exist. That list is created when the
 # plugins register themselves. This makes it trivial to add a new plugin: just
 # define the function and decorate it with @register.
# %% markdown
# #### Flask secret webpage
# %%
# from flask import Flask, g, request, redirect, url_for
# import functools
# app = Flask(__name__)

# def login_required(func):
#     """Make sure user is logged in before proceeding"""
#     @functools.wraps(func)
#     def wrapper_login_required(*args, **kwargs):
#         if g.user is None:
#             return redirect(url_for("login", next=request.url))
#         return func(*args, **kwargs)
#     return wrapper_login_required

# @app.route("/secret")
# @login_required
# def secret():
#     ...
# %% markdown
# ### Fancy decorators
# %%
# from decorators import debug, timer

class TimeWaster:
    @debug
    def __init__(self, max_num):
        self.max_num = max_num

    @timer
    def waste_time(self, num_times):
        for _ in range(num_times):
            sum([i**2 for i in range(self.max_num)])
# %%
tw = TimeWaster(1000)
# %%
tw.waste_time(999)
# %% markdown
# #### decorate the whole class
# %%
from dataclasses import dataclass

@dataclass
class PlayingCard:
    rank: str
    suit: str
# %%
pc = PlayingCard('a', 'b')
# %%
pc.rank
# %%
# from decorators import timer

@timer
class TimeWaster:
    def __init__(self, max_num):
        self.max_num = max_num

    def waste_time(self, num_times):
        for _ in range(num_times):
            sum([i**2 for i in range(self.max_num)])
# %%
tw = TimeWaster(1000)
# %%
#tw.waste_time(999)

# Nesting decorator
@debug
@do_twice
def greet(name):
    print(f"Hello {name}")
greet("Eva")

# Observe the difference if we change the order of @debug and @do_twice:
@do_twice
@debug
def greet(name):
    print(f"Hello {name}")

