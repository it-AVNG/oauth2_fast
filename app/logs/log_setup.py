import logging
import logging.config as cf
import yaml
import os



def get_log_config():
    CWD =os.getcwd()
    with open(f'{CWD}/logs/log_config.yaml', 'rt') as f:
        setting = yaml.safe_load(f.read())

    cf.dictConfig(setting)


def log(func):
    def decorator_log(*args, **kwargs):
        module_logger = logging.getLogger(f'app.{func.__name__}')
        module_logger.info(f'start {func.__name__}')
        func(*args,**kwargs)
        module_logger.info(f'stop {func.__name__}')
    return decorator_log


if __name__ == "__main__":
    get_log_config()
    logger = logging.getLogger('app.main')
    logger.warning('my 1st log')