from setuptools import setup

setup(
    name='multithreaded_image_filter',
    version='0.1',
    py_modules=['multithreaded_image_filter'],
    install_requires=[
        'opencv-python-headless',
        'numpy'
    ],
    entry_points={
        'console_scripts': [
            'mif=multithreaded_image_filter:main',
        ],
    },
)
