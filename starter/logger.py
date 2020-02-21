import pathlib

root = pathlib.Path(__file__).parent.parent
path = f'{root}/test_log.txt'

import logging
logger = logging.getLogger('neo')
hdlr = logging.FileHandler(path)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
