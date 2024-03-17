# README #

yCrash ycrash-python-agent profiles python applications capturing the system details

* Threads
* Heap
* GC
* Process
* Logs
* System Commands

### How to build and upload the module ###

1. To build 'python3.8 setup.py sdist'
2. To upload 'twine upload --verbose dist/*' ( Requires https://pypi.org/ account and setup )


### How to use ###
Just install using pip
1. install ycrash profiler
pip install ycrash-profile-dev

2. import the profiler in code
from ycrash import profiler

3. init the profiler with configuration file location

