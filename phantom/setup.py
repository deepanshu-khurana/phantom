from setuptools import setup, find_packages

setup(
    name="phantom-cli",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "colorama",
    ],
    entry_points={
        "console_scripts": [
            "phantom=phantom.main:entry_point",
        ],
    },
    author="Ghost",
    description="Cyberpunk Security Toolkit",
)
