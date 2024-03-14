# math_operations/setup.py

from setuptools import setup, find_packages

setup(
    name='math-utilsn',
    version='0.1.1',
    author='Samrat Kumar Dev Sharma',
    author_email='samratkumardev2001@gmail.com',
    description='A simple package for basic math operations',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/math_operations',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'math_operations_add = math_operations.operations:add',
            'math_operations_subtract = math_operations.operations:subtract',
            'math_operations_multiply = math_operations.operations:multiply',
            'math_operations_divide = math_operations.operations:divide',
        ],
    },
)
