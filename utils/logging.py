import logging

def log_info(message):
    logging.basicConfig(filename='redaction_tool.log', level=logging.INFO)
    logging.info(message)

def log_error(message):
    logging.basicConfig(filename='redaction_tool.log', level=logging.ERROR)
    logging.error(message)
