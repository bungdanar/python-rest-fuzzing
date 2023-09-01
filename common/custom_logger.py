import logging


def create_res_time_logger():
    res_time_logger = logging.getLogger('res_time_logger')
    res_time_logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(levelname)s: %(message)s')

    file_handler = logging.FileHandler('logs/res-time.log')
    file_handler.setFormatter(formatter)

    res_time_logger.addHandler(file_handler)

    return res_time_logger


def create_err_500_logger():
    err_500_logger = logging.getLogger('err_500_logger')
    err_500_logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(levelname)s: %(message)s')

    file_handler = logging.FileHandler('logs/err500.log')
    file_handler.setFormatter(formatter)

    err_500_logger.addHandler(file_handler)

    return err_500_logger
