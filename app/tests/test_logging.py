import sys
import os
sys.path.append(f'{os.getcwd()}')
import logging
from logs.log_setup import get_log_config, log

def test_log_config_exits():
    '''assert that the config file is included'''
    try:
        get_log_config()
    except Exception as e:
        assert not isinstance(e,FileNotFoundError)

def test_log_output(caplog):
    '''assert that the log is created and write out'''
    get_log_config()
    caplog.set_level(logging.DEBUG)
    @log
    def run_test_function():
        print('This is a test function')

    run_test_function()

    assert 'begin run_test_function' in caplog.text
    assert 'finished run_test_function' in caplog.text