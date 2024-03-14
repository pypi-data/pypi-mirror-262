import time
import threading
from .thread_profiler import capture_export_thread_data
from .heap_dump_profiler import HeapDumpCapturer
from .process_profiler import capture_print_process_details
from .mem_profiler import ycrash_memory_extract
from .log_profiler import upload_log_data
from .system_profiler import export_all_system_data
import platform
import yaml
import logging


global_config_data = None

def ycrash_init(configFilePath):
    thread_states_thread = threading.Thread(target=profile_data, args=(configFilePath,), name="yCrash.analyzer")
    thread_states_thread.start()


def profile_data(configFilePath):
    ycrashConfig = load_config(configFilePath)
    #profile_all_methods()
    #find_all_modules()
    #gc.set_debug(gc.DEBUG_LEAK))
    print(ycrashConfig.get('options', {}).get('m3Frequency'))
    while True:
        log()
        upload_log_data(ycrashConfig)
        export_all_system_data(ycrashConfig)
        capture_export_thread_data(ycrashConfig)
        capturer = HeapDumpCapturer()
        capturer.capture_heap_dump(ycrashConfig)
        capture_print_process_details(ycrashConfig)
        ycrash_memory_extract(ycrashConfig)
        time.sleep(ycrashConfig.get('options', {}).get('m3Frequency'))


def log():
    logging.debug('This is a debug message')
    logging.info('This is an info message')
    logging.warning('This is a warning message')
    logging.error('This is an error message')
    logging.critical('This is a critical message')


def load_config(configFilePath):
    try:
        # Read the YAML file
        with open(configFilePath, 'r') as file:
            print(file)
            data = yaml.safe_load(file)
        # Accessing attributes
        version = data.get('version')
        options = data.get('options', {})

        # Accessing specific attributes within options
        k = options.get('k')
        s = options.get('s')
        a = options.get('a')
        m3Frequency = options.get('m3Frequency')
        app_logs = options.get('appLogs', [])

        # Outputting the values
        print("Version:", version)
        print("k:", k)
        print("s:", s)
        print("a:", a)
        print("m3Frequency:", m3Frequency)

    except FileNotFoundError:
        print("File not found:", configFilePath)
        return None

    except yaml.YAMLError as exc:
        print("Error parsing YAML:", exc)
        return None

    return data



