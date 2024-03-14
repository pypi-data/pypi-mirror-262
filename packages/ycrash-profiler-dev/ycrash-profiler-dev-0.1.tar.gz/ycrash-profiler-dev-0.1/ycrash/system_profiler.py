import logging

from .common import run_command, get_current_pid, run_interactive_command
from .webclient import upload_json_data
import json
from .common import getKey, getServerUrl
from .system_info import SystemInfo
from .system_commands import BaseCommands

PS_DUMP_ENDPOINT = "/cm-receiver&dt=ps"
DF_DUMP_ENDPOINT = "/cm-receiver&dt=df"
NETSTAT_DUMP_ENDPOINT = "/cm-receiver&dt=ns"
KERNAL_DUMP_ENDPOINT = "/cm-receiver&dt=kernal"
TOP_DUMP_ENDPOINT = "/cm-receiver&dt=top"
DMSEG_DUMP_ENDPOINT = "/cm-receiver&dt=dmesg"
PING_DUMP_ENDPOINT = "/cm-receiver&dt=ping"
VMSTAT_DUMP_ENDPOINT = "/cm-receiver&dt=vmstat"

system_info = SystemInfo()
commands_manager = BaseCommands(system_info.get_os_name())


def export_all_system_data(config):
    capture_and_upload_system_commands(config, PS_DUMP_ENDPOINT , commands_manager.PS)
    capture_and_upload_system_commands(config, DF_DUMP_ENDPOINT, commands_manager.Disk)
    capture_and_upload_system_commands(config, NETSTAT_DUMP_ENDPOINT, "netstat -an")
    capture_and_upload_system_commands(config, TOP_DUMP_ENDPOINT, commands_manager.Top)
    capture_and_upload_system_commands(config, DMSEG_DUMP_ENDPOINT, commands_manager.DMesg)
    capture_and_upload_system_commands(config, KERNAL_DUMP_ENDPOINT,  commands_manager.KernelParam)
    capture_and_upload_system_commands(config, KERNAL_DUMP_ENDPOINT,  commands_manager.VMState)

def capture_and_upload_system_commands(config, endpoint, command):
    logging.debug(f"endpoint {endpoint} id {id} command {command}")
    data = {
        "data": run_command(command),
    }
    system_details_json = json.dumps(data, indent=4)
    upload_json_data('application/json', getKey(config), getServerUrl(config, endpoint),
                     system_details_json)
