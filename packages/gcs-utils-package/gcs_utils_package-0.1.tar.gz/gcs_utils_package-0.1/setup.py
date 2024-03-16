from setuptools import setup, find_packages

setup(
    name="gcs_utils_package",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "google-cloud-storage",
        "Pillow"
    ],
)