# main.py

from cli import *
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s:  [%(module)s] - %(message)s')

if __name__ == '__main__':
    cli()