import functools
import asyncio

from aiohttp.http_exceptions import HttpProcessingError

from tools import LoggerHelper

logger = LoggerHelper.get_logger(name="decorator", module="parse", error=True)


class ParseDecorator:
    @staticmethod
    def log_call(prefix):
        def decorator(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                try:
                    result = await func(*args, **kwargs)

                    return result
                except HttpProcessingError as e:
                    logger.error(msg=f"CAll: {prefix} Http Process Error: {e}, data: {args}, {kwargs}", exc_info=True)
                except Exception as e:
                    logger.error(msg=f"CAll: {prefix} Http Exception: {e}", exc_info=True)

                return None

            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                try:
                    result = func(*args, **kwargs)

                    return result
                except HttpProcessingError as e:
                    logger.error(msg=f"CAll: {prefix} Http Process Error: {e}, data: {args}, {kwargs}", exc_info=True)
                except Exception as e:
                    logger.error(msg=f"CAll: {prefix} Http Exception: {e}", exc_info=True)

                return None

            return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

        return decorator
