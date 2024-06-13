from setuptools import find_packages
from setuptools import setup

setup(
    name='stretch_seeing_eye_ros2',
    version='0.0.0',
    packages=find_packages(
        include=('stretch_seeing_eye_ros2', 'stretch_seeing_eye_ros2.*')),
)
