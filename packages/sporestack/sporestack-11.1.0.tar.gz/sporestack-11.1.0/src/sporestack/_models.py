# This file is split out to improve CLI performance.
from enum import Enum


class Currency(str, Enum):
    xmr = "xmr"
    """Monero"""
    btc = "btc"
    """Bitcoin"""
    bch = "bch"
    """Bitcoin Cash"""
