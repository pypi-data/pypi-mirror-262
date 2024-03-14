# from pkg_resources import parse_requirements
from setuptools import find_packages, setup



setup(
    name="blackboxai",
    version="0.7",
    packages=find_packages(),
    package_dir = {'': '.'},
    include_package_data=True,
    setup_requires= ['requests'],
    entry_points={
        "console_scripts": [
            "blackboxai = blackboxai:runChat"
        ]
    }
)