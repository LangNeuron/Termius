# core/loger.py


def get_logger():
    from os import mkdir
    from os.path import exists
    import logging
    from logging.handlers import RotatingFileHandler
    import colorlog

    logger = logging.getLogger("logger")

    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.DEBUG)  # взять уровень из yml file

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)

    if not exists("logs"):
        mkdir("logs")

    file_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=1024 * 1024 * 5,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Настройка colorlog для цветного вывода в консоль
    console_handler = logging.StreamHandler()
    color_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
    )
    console_handler.setFormatter(color_formatter)
    logger.addHandler(console_handler)

    return logger
