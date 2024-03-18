from nlogging import nLogging
from nlogging import DEBUG, INFO, WARNING, ERROR, CRITICAL, NOOUT


def subfunc1():
	logging.output(DEBUG, 'message for debugging.')
	logging.output(CRITICAL, 'message for critical!')

def subfunc2():
	logging.output(DEBUG, 'message for debugging.')
	logging.output(CRITICAL, 'message for critical!')


# Initializing for nLogging
logging = nLogging('YourLoggerName', './sample.log')
logging.set_out_level(stream_lv=DEBUG, file_lv=DEBUG)

logging.output(DEBUG, 'message for debugging.')
logging.output(CRITICAL, 'message for critical!')


# You can chang log-lv(stream_lv: DEBUG -> INFO, file_lv: DEBUG -> INFO)
logging.set_out_level(stream_lv=INFO, file_lv=INFO)
subfunc1()

# You can chang log-lv(stream_lv: INFO -> NOOUT, file_lv: INFO -> WARNING)
logging.set_out_level(stream_lv=NOOUT, file_lv=WARNING)
subfunc2()
