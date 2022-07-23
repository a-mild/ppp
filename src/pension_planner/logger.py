import logging

bus_logger = logging.getLogger("bus_logger")
file_handler = logging.FileHandler("bus.log")
bus_logger.addHandler(file_handler)
bus_logger.setLevel(logging.DEBUG)
