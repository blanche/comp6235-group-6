import logging
import re


def convert_to_int_and_store(array, attribute):
    if attribute in array and isinstance(array[attribute], str):
        try:
            array[attribute] = int(array[attribute])
        except ValueError:
            array[attribute] = None


def setup_logger(name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(level)
    logger.addHandler(stream_handler)
    return logger


restaurant_stopwords = ["ltd", "limited", "southampton", "the", "restaurant", "bar", "coffee", "and"]
name_clean_re = re.compile("[^ A-Za-z0-9]+")
