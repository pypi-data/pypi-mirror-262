from setuptools import setup, find_packages

setup(
    name='ycrash-profiler-dev',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    description='yCrash Python Agent',
    install_requires=['pyyaml', 'guppy3', 'requests', 'memory_profiler','psutil','pexpect'],
    url='https://ycrash.io',
    author='YCrash Team',
    author_email='team@tier1app.com'
)
