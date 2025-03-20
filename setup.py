from setuptools import setup, find_packages  # type: ignore

setup(
    name="main",
    version="0.1.0",
    # py_modules=["main"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
        "Pillow",
        "click-extra",
    ],
    entry_points={
        "console_scripts": [
            "snow = snow.main:cli",
        ],
    },
)
