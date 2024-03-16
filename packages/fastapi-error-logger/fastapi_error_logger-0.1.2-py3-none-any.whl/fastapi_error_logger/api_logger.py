# api_logger.py

import json
import logging
import traceback
from datetime import datetime, timedelta, timezone
from fastapi import Request
import inspect
import os
from logging.handlers import RotatingFileHandler
import uuid

from fastapi_error_logger.models import ApiErrorLog, SessionLocal


async def log_api_error(
	request: Request,
	status_code=200,
	req_body={},
	function_name="",
	personalized_message="",
):
	try:
		# req_body = await request.body()
		function_name = (
			function_name
			if function_name
			else inspect.currentframe().f_back.f_code.co_name
		)
		api_title = function_name.split("?")[0].replace("_", " ").title() + " API Error"
		api_title = "/".join(api_title.split("/")[-2:])
		req_time = datetime.now(timezone(timedelta(hours=5, minutes=30)))

		# Create a dictionary with error log data
		data = {
			"req_body": req_body,
			# "req_body": req_body.decode(),
			"path_params": str(request.path_params),
			"query_params": str(request.query_params),
			"headers": dict(request.headers),
			"api_url": str(function_name),
			"api_title": api_title,
			"traceback": traceback.format_exc(),
			"personalized_message": personalized_message,
			"client_ip": request.client,
			"status_code": status_code,
			"req_time": str(req_time),
		}

		# Save error log to the database
		data["headers"] = json.dumps(data["headers"])

		# log_to_json('api_error_log.json', data)
		save_error_log_to_db(data)
	except Exception as e:
		logging.exception("An error occurred while logging API error: {}".format(str(e)))



def log_to_json(log_file_path, data):
	try:
		logs = []

		if os.path.exists(log_file_path):
			with open(log_file_path, "r") as f:
				logs = json.load(f)

		logs.append(data)

		with open(log_file_path, "w") as f:
			json.dump(logs, f)
	except Exception as e:
		logging.exception("An error occurred while writing to JSON file: {}".format(str(e)))


def setup_logger(log_file, name, log_dir="logs", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", max_log_size=100 * 1024 * 1024, backup_count=3):
	if not os.path.isdir(log_dir):
		try:
			os.mkdir(log_dir)  
		except OSError as error:  
			raise error

	log_file = log_dir + "/" + log_file
	handler = RotatingFileHandler(
		log_file, maxBytes=max_log_size, backupCount=backup_count, 
	)

	formatter = logging.Formatter(format)
	handler.setFormatter(formatter)

	logger = logging.getLogger(name)
	logger.addHandler(handler)

	return logger

def save_error_log_to_db(data):
	"""
	Function to save error log data to the database using the provided ORM session.
	"""
	error_log = ApiErrorLog(error_id=str(uuid.uuid4()), **data)

	# Add the error log to the database and commit the transaction
	with SessionLocal() as db:
		repeated_error_log = (
			db.query(ApiErrorLog)
			.filter(ApiErrorLog.traceback == error_log.traceback)
			.first()
		)
		if repeated_error_log:
			error_log.status = "Repeated"
		db.add(error_log)
		db.commit()