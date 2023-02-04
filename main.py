#!/usr/bin/env python

from src.parse_config import get_config
from src.generator import DataGenerator

if __name__ == "__main__":
    conf = get_config("test2.yaml")
    DataGenerator(conf).run()
