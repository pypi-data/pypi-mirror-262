from setuptools import setup, find_packages

setup(
    name="vmanage_rest_session",
    version="1.0.8",
    author="demyang",
    author_email="demyang@cisco.com",
    description="vmanage restapi session",
    url="https://sdwan-git.cisco.com/crdc-tools/vmanage_rest_session",
    packages=find_packages(exclude=("contrib",)),
    zip_safe=True,
    include_package_data=True
)
