#!/usr/bin/env python

from src.parser import get_config
from src.generator import DataGenerator

conf = get_config("test2.yaml")
DataGenerator(conf).run()
