from setuptools import setup, find_packages

setup(
    name="gcs_utils_package",
    version="0.3",
    packages=find_packages(),
    python_requires=">=3.8.0",
    install_requires=[
        "google-cloud-storage",
        "Pillow"
    ],
)