import os
import logging
import json
import time
from .webclient import upload_json_data
from .common import getKey, getServerUrl

LOG_DUMP_ENDPOINT = "/cm-receiver+&dt=td"

def upload_log_data(config):
    if config.get('options', {}).get('appLogs') is not None:
        log_path = config.get('options', {}).get('appLogs')
    else:
        log_path = get_log_file_location()

    logBackUpFile = log_path + '.ycrash.bak'
    if not os.path.exists(logBackUpFile):
        with open(logBackUpFile, 'w'):
            pass

    with open(logBackUpFile, 'r') as old_log_file:
        old_log_lines = set(old_log_file.readlines())

    with open(log_path, 'r') as new_log_file:
        new_log_lines = set(new_log_file.readlines())

    new_additions = new_log_lines - old_log_lines
    copy_file(log_path, logBackUpFile)

    log_lines = json.dumps(list(new_additions), indent=4)

    log_json = {
        "captureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "logs": log_lines
    }

    upload_json_data('application/json', getKey(config), getServerUrl(config,LOG_DUMP_ENDPOINT) , json.dumps(log_json,indent=4))



def get_log_file_location():
    # Get the root logger
    root_logger = logging.getLogger()

    # Iterate over all handlers of the root logger
    for handler in root_logger.handlers:
        # Check if the handler is a FileHandler
        if isinstance(handler, logging.FileHandler):
            # Return the log file's absolute path
            return handler.baseFilename

    # If no FileHandler is found, return None or any other value you prefer
    return None


def copy_file(source_file, destination_file):
    try:
        # Open the source file in binary mode for reading
        with open(source_file, 'rb') as src_file:
            # Open the destination file in binary mode for writing
            with open(destination_file, 'wb') as dest_file:
                # Read the content of the source file and write it to the destination file
                dest_file.write(src_file.read())
        print("File copied successfully.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
