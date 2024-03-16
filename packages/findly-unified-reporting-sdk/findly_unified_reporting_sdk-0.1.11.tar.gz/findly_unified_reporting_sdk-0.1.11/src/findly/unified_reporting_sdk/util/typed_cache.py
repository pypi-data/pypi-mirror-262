from typing import TypeVar, Callable, Any, Optional, Type
from functools import wraps
from aiocache import BaseCache, cached as aiocache_cached

T = TypeVar('T')


def typed_cache(
        ttl: Optional[int] = None,
        cache: Optional[Type[BaseCache]] = None,
        skip_cache_func: Optional[Callable[[Any], bool]] = None
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    A type-preserving caching decorator that allows configuration of the cache behavior.

    Args:
        ttl (int): Time to live for the cache entries.
        cache (str): The cache alias to use.
        skip_cache_func (Callable[[Any], bool]): A function to determine if the cache should be skipped.

    Returns:
        A decorator that caches the results of the decorated function.
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        # Apply the aiocache cached decorator with the provided arguments
        cached_func = aiocache_cached(ttl=ttl, cache=cache, skip_cache_func=skip_cache_func)(func)

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            return cached_func(*args, **kwargs)

        return wrapper

    return decorator
