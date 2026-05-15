"""Advanced Python Concepts: Custom Decorators.
Provides decorators for wrapping functions in error handlers and timing execution.
"""
import functools
import time

def handle_cli_errors(func):
    """A decorator that wraps CLI functions to catch common errors and output cleanly.
    
    Args:
        func: The function to be wrapped.
        
    Returns:
        The wrapped function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            print(f"\033[91mInput Error: {ve}\033[0m")
        except KeyboardInterrupt:
            print("\n\033[93mOperation cancelled by user.\033[0m")
        except Exception as e:
            print(f"\033[91mAn unexpected error occurred: {e}\033[0m")
    return wrapper

def time_execution(func):
    """A decorator that prints the execution time of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"\033[90m[Debug] {func.__name__} took {end - start:.4f} seconds.\033[0m")
        return result
    return wrapper
