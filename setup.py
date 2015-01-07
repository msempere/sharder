from setuptools import setup

setup(name='sharder',
    version='0.1',
    description='Tiny sharding for Redis',
    url='https://github.com/msempere/sharder',
    author='msempere',
    author_email='msempere@gmx.com',
    license='MIT',
    packages=['sharder'],
    test_suite="tests",
    zip_safe=False)
