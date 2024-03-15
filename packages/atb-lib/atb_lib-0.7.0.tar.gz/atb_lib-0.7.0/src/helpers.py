﻿import asyncio
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
