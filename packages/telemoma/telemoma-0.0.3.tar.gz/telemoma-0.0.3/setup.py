# read the contents of your README file
from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    lines = f.readlines()

# remove images from README
lines = [x for x in lines if ".png" not in x]
long_description = "".join(lines)

setup(
    name="telemoma",
    version="0.0.3",
    author="Shivin Dass",
    author_email='shivindass@gmail.com',
    description='A modular and versatile teleoperation system for mobile manipulation',
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/UT-Austin-RobIn/telemoma",
    install_requires=[
        "numpy~=1.23.5",
        "opencv-python~=4.8.1",
        "mediapipe~=0.10.9",
        "scipy~=1.10.1",
        "pyrealsense2",
        "pyspacemouse",
        "pynput~=1.7.6",
        "matplotlib~=3.7.1",
        "gym~=0.26.2",
    ],
    packages=["telemoma"],
    python_requires=">=3",
) 
