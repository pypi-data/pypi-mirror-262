import datetime
import os
import inspect
from logging import getLogger, StreamHandler, FileHandler, Formatter
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
#==========================================================================
# nLogging - A Simple logging Liblary   version 0.1.0
#
#   FORMAT: YYYY/MM/DD hh:mm:ss.sss LEVEL Filename(LineNo) [FuncName] message
#
# Copyright© 2024 matsutaka@norageek All Rights Reserved.
# Released under the MIT License
# https://opensource.org/licenses/mit-license.php
#==========================================================================

NOOUT = CRITICAL + 100

class nLogging:

#--------------------------------------------------------------------------
# constructor
#--------------------------------------------------------------------------
	def __init__(self, logging_name: str, logfile_name='') -> None:
		self._logger = getLogger(logging_name + '_logger')
		self._logger.setLevel(DEBUG)

		self._h_stream = StreamHandler()
		self._h_stream.setLevel(DEBUG)

		if logfile_name == '':
			self._h_file = FileHandler(filename="{}.log".format(logging_name), encoding="utf-8")
		else:
			self._h_file = FileHandler(filename=logfile_name, encoding="utf-8")
		self._h_file.setLevel(DEBUG)

		self._logger.addHandler(self._h_stream)
		self._logger.addHandler(self._h_file)

#--------------------------------------------------------------------------
# destructor
#--------------------------------------------------------------------------
	def __del__(self) -> None:
		pass

#--------------------------------------------------------------------------
# File name setting
#--------------------------------------------------------------------------
	def set_filename(self, file_name: str):
		if self._h_file != None:
			self._logger.removeHandler(self._h_file)
		self._h_file = FileHandler(filename=file_name, encoding="utf-8")
		self._logger.addHandler(self._h_file)

#--------------------------------------------------------------------------
# Logging level(Threshold) setting
#--------------------------------------------------------------------------
	def set_out_level(self, stream_lv=None, file_lv=None):
		if stream_lv is not None:
			self._h_stream.setLevel(stream_lv)
		if file_lv is not None:
			self._h_file.setLevel(file_lv)

#--------------------------------------------------------------------------
# output message
#--------------------------------------------------------------------------
	def output(self, level: int, message: str):
		log_proc = None

		frame = inspect.currentframe().f_back
		file_name = os.path.basename(frame.f_code.co_filename)
		func_name = frame.f_code.co_name
		line_no = frame.f_lineno

		outlevel = 'Unknown '
		now_time = datetime.datetime.now()
		log_time = now_time.strftime('%Y/%m/%d %H:%M:%S') + '.{:03d}'.format(now_time.microsecond // 1000)
		if level == DEBUG:
			log_proc = self._logger.debug
			outlevel = 'DEBUG   '
		elif level == INFO:
			log_proc = self._logger.info
			outlevel = 'INFO    '
		elif level == WARNING:
			log_proc = self._logger.warning
			outlevel = 'WARNING '
		elif level == ERROR:
			log_proc = self._logger.eror
			outlevel = 'ERROR   '
		elif level == CRITICAL:
			log_proc = self._logger.critical
			outlevel = 'CRITICAL'

		if log_proc != None:
			logging_text = '{} {} {}({}) [{}] {}'.format(log_time, outlevel, file_name, line_no, func_name, message)
			log_proc(logging_text)

