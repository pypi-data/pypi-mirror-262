import asyncio
import inspect
import os
import sys
import zlib
from decimal import Decimal

import arrow
import msgpack


def ts_to_dt_str_with_ms(timestamp_ms):
    dt = arrow.get(timestamp_ms / 1000)
    return dt.format('YYYY-MM-DD HH:mm:ss.SSS')


def pack_and_compress(data):
    return zlib.compress(msgpack.packb(data))


def decompress_and_unpack(data):
    return msgpack.unpackb(zlib.decompress(data))


async def async_pack_and_compress(data):
    return await asyncio.to_thread(lambda: zlib.compress(msgpack.packb(data)))


async def async_decompress_and_unpack(data):
    return await asyncio.to_thread(lambda: msgpack.unpackb(zlib.decompress(data)))


def find_current_avg_price(bids, asks):
    max_bid_price = Decimal(bids[0][0]) if bids else None
    min_ask_price = Decimal(asks[0][0]) if asks else None

    if max_bid_price and min_ask_price:
        return str((max_bid_price + min_ask_price) / 2)
    elif max_bid_price:
        return str(max_bid_price)
    elif min_ask_price:
        return str(min_ask_price)
    else:
        return None


def update_sys_path():
    # Update sys.path to include 'src' directory and parent directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(current_dir, 'src'))
    sys.path.append(os.path.dirname(current_dir))


async def close_resource(resource, logger):
    resource_name = repr(resource)  # Get a string representation of the resource
    logger.info(f"Closing resource {resource_name}")
    if hasattr(resource, "close"):  # Check if resource has a close method
        try:
            if inspect.iscoroutinefunction(resource.close):
                await resource.close()  # If the close method is async
            else:
                resource.close()  # If the close method is not async
        except Exception as e:
            logger.error(f"Error closing {resource_name}: {e}")
        else:
            logger.info(f"Successfully closed the resource {resource_name}.")
    else:
        logger.warning(f"{repr(resource_name)} does not have a close method.")


async def close_resources(resources, logger):
    logger.info("Closing all resources...")
    # Start all the close operations, they will run concurrently
    close_ops = [close_resource(resource, logger) for resource in resources]
    await asyncio.gather(*close_ops)
    logger.info("All resources closed.")


def convert_to_scaled_integer(number, scaling_factor: Decimal):
    return int(Decimal(number) * scaling_factor)


def unscale_number(scaled_number, scaling_factor: Decimal):
    return Decimal(scaled_number) / scaling_factor
