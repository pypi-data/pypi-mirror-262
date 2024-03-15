from setuptools import setup, find_packages

VERSION = '0.1.1'
DESCRIPTION = 'Fix bugs'
LONG_DESCRIPTION = 'Fix bugs in load_vicuna_13b'

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
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
            'Topic :: Software Development :: Libraries'
        ]
)