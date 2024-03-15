from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A tool to load models for fact'
LONG_DESCRIPTION = 'Help to load models like Vicuna, LLaMa.'

setup(
        name='factools',
        version=VERSION,
        author='Song JiaXuan',
        author_email='songjx@bupt.edu.cn',
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['transformers', 'typing', 'torch'],
        keywords=['python', 'load', 'LLM'],
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
        ]
)