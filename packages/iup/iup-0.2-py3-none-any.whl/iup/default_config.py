#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from configparser import ConfigParser


DEFAULT_CONFIG = '''[common]
host = 192.168.1.1
port = 22
username = root
password = 123457
refresh = False'''


def write_default_config(path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(DEFAULT_CONFIG)

def write_config(config: ConfigParser, path):
    with open(path, 'w', encoding='utf-8') as f:
        config.write(f)