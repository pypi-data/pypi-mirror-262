from setuptools import setup, find_packages

setup(
    name="gcs_utils_package",
    version="0.4",
    packages=["gcs_utils_package"],
    python_requires=">=3.8.0",
    install_requires=[
        "google-cloud-storage",
        "Pillow"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ]
)