import psutil
import json
from .common import get_current_pid
from .webclient import upload_json_data
from .common import  getKey, getServerUrl


def get_io_details(io_counter):
    try:
        # Create a dictionary with I/O details
        io_dict = {
            "read_count": io_counter.read_count,
            "write_count": io_counter.write_count,
            "read_bytes": io_counter.read_bytes,
            "write_bytes": io_counter.write_bytes
        }
        # Convert the dictionary to a JSON-formatted string
        io_json = json.dumps(io_dict, indent=4)
        return io_json
    except psutil.Error as e:
        # Handle potential exceptions from psutil
        print(f"Error getting I/O details: {e}")
        return None


def capture_print_process_details(config):
    try:
        process = psutil.Process(get_current_pid())
        process_data = {
            "pid": get_current_pid(),
            "cpu_percent": process.cpu_percent(interval=1),
            "memory_info": process.memory_info()._asdict(),
            "connections": len(process.connections()),
            "threads_count": len(process.threads()),  # Count the number of threads
            "threads_cpu_percentage": get_threads_cpu_percent(process),
        }
        process_details = {"process_details": process_data}
        json_data = json.dumps(process_details, indent=4)
        upload_json_data('application/json', getKey(config), getServerUrl(config) + "/python/process_details", json_data)
    except psutil.NoSuchProcess:
        print(f"Process with PID {get_current_pid()} not found.")
    except Exception as e:
        print(f"Error: {e}")


def get_threads_cpu_percent(p):
    threadList = []
    for thread in p.threads():
        total_percent = p.cpu_percent(0.1)
        total_time = sum(p.cpu_times())
        cpu_percentage = total_percent * ((thread.system_time + thread.user_time) / total_time)
        process_data = {'id': thread.id,
                        'cpu_percentage': cpu_percentage}

        threadList.append(process_data)
    return threadList
