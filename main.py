#!/usr/bin/env python
"""
main.py.

    A driver for data_maker in development.
"""

from src.generator import DataGenerator
from src.parse_config import get_config

if __name__ == "__main__":
    conf = get_config("test2.yaml")
    DataGenerator(conf).run()
