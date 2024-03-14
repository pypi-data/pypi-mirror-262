import tracemalloc
import json
from guppy import hpy
from .webclient import upload_json_data
from .common import  getKey, getServerUrl

HEAP_DUMP_ENDPOINT = "/cm-receiver+&dt=hd"

class HeapDumpCapturer:
    def __init__(self):
        tracemalloc.start()

    def capture_heap_dump(self, config):
       #print(f"YC Config:{config}")
       heapDumpJson = {'heapDumpFormat1':
                        capture_heap_tracemalloc_dump(self),
                       'heapDumpFormat2':
                        f"\'{capture_heap_guppy_dump(self)}\'"
                        }
       upload_json_data('application/json', getKey(config), getServerUrl(config,HEAP_DUMP_ENDPOINT), heapDumpJson)
       #print(f'uploaded json {heapDumpJson} with key {key}')

def capture_heap_tracemalloc_dump(self, top_n=10):
        snapshot = tracemalloc.take_snapshot()
        stats = snapshot.statistics('lineno')

        # Convert stats to a list of dictionaries
        heap_dump = [{
            'filename': stat.traceback[0].filename,
            'lineno': stat.traceback[0].lineno,
            'sizeInBytes': stat.size,
            'noOfTimesCalled': stat.count
        } for stat in stats[:top_n]]

        heapDumpList = []
        for entry in heap_dump:
            heapDumpList.append(json.dumps(entry, indent=4))
        return heapDumpList

def capture_heap_guppy_dump(self):
    hp = hpy()
    heap: object = hp.heap()
    print(heap)
    return heap
