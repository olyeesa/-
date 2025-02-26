import logging

def setup_logger():
    logger = logging.getLogger("SMSLogger")
    handler = logging.FileHandler("sms_sender.log")
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

logger = setup_logger()
